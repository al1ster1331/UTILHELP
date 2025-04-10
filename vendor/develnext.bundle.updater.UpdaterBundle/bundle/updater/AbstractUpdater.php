<?php
namespace bundle\updater;

use bundle\updater\Updater;
use php\compress\ZipFile;
use php\framework\Logger;
use php\io\File;
use php\io\FileStream;
use php\io\MiscStream;
use php\io\Stream;
use php\lang\Process;
use php\lang\System;
use php\lang\Thread;
use php\lib\arr;
use php\lib\fs;
use php\lib\str;
use php\net\NetStream;

/**
 * Абстрактный класс для сервиса обновлений 
 */
abstract class AbstractUpdater {
    
    /**
     * Сообщение, которое будет отправлено программе-родителю,
     * которое будет являться сигналом для завершения работы 
     */
    const CLOSE_MESSAGE = 'updateRequired!';
    
    /**
     * Текущая версия программы
     * @var string 
     */
    protected $currentVersion = '1.0.0.0';
        
    /**
     * Временный файл
     * @var string 
     */
    protected $tempFile = 'update.tmp'; 
           
    /**
     * Файл приложения родителя
     * @var string 
     */
    protected $origFile;
    
    public function __construct(){
        $this->tempFile = self::getCurrentDir() . $this->tempFile;
    }
    
    /**
     * Указать текущую версию программы
     */
    public function setCurrentVersion($version){
        $this->currentVersion = $version;
    }    

    /**
     * Указать путь к временному файлу
     */
    public function setTempFile(string $tempFile){
        $this->tempFile = $tempFile;
        File::of($this->tempFile)->createNewFile(true);
    } 
    
    /**
     * Указать имя исполняемого файла приложения родителя
     */
    public function setOrigFile(string $origFile){
        $this->origFile = self::getCurrentDir() . basename($origFile);
    }    
    
    /**
     * Отправить приложению-родителю сигнал на завершение работы 
     */
    public function closeParentApplication(){
        $stream = new MiscStream('stdout');
        $stream->write(self::CLOSE_MESSAGE);
        $stream->flush();
        $stream->close(); // Мешает дебагу, но необходимо для релизной версии
    }
    
   
    /**
     * Сравнить версию с текущей
     * @return bool - eсли true, версия $version старше текущей
     */
    public function compareVersion($version) : bool {
        $c = explode('.', $this->currentVersion);
        $r = explode('.', $version);

        for($i = 0; $i < 4; ++$i){
            $c[$i] = str::format('%03d', intval(isset($c[$i])?$c[$i]:0));
            $r[$i] = str::format('%03d', intval(isset($r[$i])?$r[$i]:0));
        }

        $current = intval(implode('', $c));
        $require = intval(implode('', $r));

        //var_dump('!!!Current version: ' . $this->currentVersion . ' (weight='.$current.')');
        //var_dump('!!!New version: ' . $version . ' (weight='.$require.')');

        return $require > $current;
    }
    
    /**
     * Буфер для загрузки файла
     * @var int
     */
    protected $buffer = 256 * 1024;
    
    /**
     * Скачать и установить обновление
     * @param string $url Прямая ссылка для загрузки
     * @param string $filename Имя загружаемого файла (только имя, без пути)
     * @param int $totalSize Размер скачиваемого файла (в байтах)
     * @param callable $progress Функция, которая будет вызываться по мере установки обновления: @
     *     @args[0] string $status = download|install|complete
     *     @args[1] int $progress = 0..100
     *     
     * @async Функция выполняется в отдельном потоке не тормозя GUI
     */
    protected function applyUpdate(string $url, string $filename, int $totalSize = 0, callable $progress){
        (new Thread(function() use ($url, $filename, $totalSize, $progress){
            $cd = self::getCurrentDir();
            $save = FileStream::of($this->tempFile, 'w');
            $download = NetStream::of($url);
            
            // Скачиваем файл
            $save->write($download->read(1));
            $length = 1;
            while(!$download->eof()){
                $data = $download->read($this->buffer);
                $save->write($data);
                $length += str::length($data);
                $percent = ($totalSize > 0) ? round($length/$totalSize*100) : 0 ;
                $this->uiCall($progress, ['download', $percent]); // Конечно же не забываем про прогресс
            }
            
            $save->close();
            $download->close();
            
            if(fs::ext($filename) == 'zip'){
                // Если мы скачали архив, его нужно распаковать
                $zip = new ZipFile($this->tempFile);
                $files = $zip->statAll();
                $total = sizeof($files);
                foreach ($files as $k => $stat){
                    if($stat['directory']) continue;
                    
                    $zip->read($stat['name'], function($stat, Stream $stream) use ($cd){
                        
                        $extractPath = $cd . $stat['name'];
                        if(fs::exists($extractPath)){
                            fs::delete($extractPath);
                        } else {
                            File::of($extractPath)->createNewFile(true);
                        }
                        
                        fs::copy($stream, $extractPath);
                    });
                    $this->uiCall($progress, ['install', round($k/$total*100)]);
                } 
               fs::delete($this->tempFile); 
            } else {
                // Если расширение другое - просто копируем этот файл в папку
                $this->uiCall($progress, ['install', 0]);
                $replaceFile = $cd . $filename;
                if(fs::exists($replaceFile)){
                    fs::delete($replaceFile);
                }
                fs::move($this->tempFile, $replaceFile);
                $this->uiCall($progress, ['install', 100]);
            }       
            $this->uiCall($progress, ['complete', 100]);
            
            // Запускаем ранее завершённую программу
            if(fs::exists($this->origFile)){
            	self::launchApp($this->origFile);
        	}
        }))->start();
    }
    
    /**
     * Запуск callback-функции в GUI потоке
     * (сделал для удобства, чтоб не плодить uiLater...) 
     */
    protected function uiCall(callable $callback, array $args = []){
        uiLater(function() use ($callback, $args){
            call_user_func_array($callback, $args);
        });
    }
    
    /**
     * В некоторых случаях, в Windows в частности, неправильно определяется путь к текущей директории,
     * ./ может восприниматься программой как путь к системной директории (Win: system32), бывает это, 
     * когда программа запущена из автозапуска или от имени администратора.
     * Данная функция парсит из системной переменной директорию, где находится исполняемый файл.
     * 
     * !!! ВНИМАНИЕ !!! Эта функция НЕ работает если при сборке программы НЕ ОТМЕЧЕНА галочка "Объединить все исходники в один исполняемый файл"
     */
    public static function getCurrentDir() : string {
        $path = System::getProperty("java.class.path");
        $sep = System::getProperty("path.separator");
        return dirname(realpath(str::split($path, $sep)[0])) . '/';
    }    

    /**
     * Возвращает путь к JVM
     */
    public static function getJavaPath() : string {
         return System::getProperty('java.home') . '/bin/java';
    }

    /**
     * Запуск приложения. Если передан путь к jar, то он будет запущен с помощью java
     */
    public static function launchApp(string $path, array $args = []) : Process {
         $command = (fs::ext($path) == 'jar')? 
         				[self::getJavaPath(), '-jar', $path]: 
         				[$path];
         $command = array_merge($command, $args);

         // Если аргумент содержит пробел, он должен быть заключён в кавычки
         foreach ($command as $key => $value) {
         	if(str::contains($value, ' ')){
         		$command[$key] = '"' . $value . '"';
         	}
         }

         return (new Process($command))->start();
    }
}