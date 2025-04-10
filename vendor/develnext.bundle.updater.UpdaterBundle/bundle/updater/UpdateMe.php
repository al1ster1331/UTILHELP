<?php
namespace bundle\updater;

use bundle\updater\GitHubUpdater;
use Exception;
use php\framework\Logger;
use php\lang\Process;
use php\lang\Thread;
use php\lib\fs;
use php\lib\str;

/**
 * Класс для обновляемого приложения 
 */
class UpdateMe 
{
    /**
     * Запустить проверку обновлений 
     * @param string $version Текущая версия программы
     * @param string $updaterFile Путь к файлу Updater.jar
     * @param callable $callback Будет вызван, если обновлений нет и updater завершил работу
     */
    public static function start(string $version, string $updaterFile = null, callable $callback = null){
        // Если путь не указан - по умолчанию файл расположен рядом с программой
        $updaterFile = is_null($updaterFile) ? GitHubUpdater::getCurrentDir() . 'Updater.jar' : $updaterFile;

        if(!fs::exists($updaterFile)){
            throw new Exception('Updater file does not found: ' . $updaterFile);
            return;
        }
        
        (new Thread(function() use ($version, $updaterFile, $callback){
            // Передаём в Updater версию программы и путь к исполняемому файлу и читаем ответ            
            $process = GitHubUpdater::launchApp($updaterFile, [$version, $GLOBALS['argv'][0]]);
            $return = $process->getInput()->readFully();
            if(str::contains($return, GitHubUpdater::CLOSE_MESSAGE)){
                // Если была получена команда на завершение работы - закрываем приложение
                // Если не завершить работу, updater не сможет заменить файлы
                Logger::info('Shutdown before updating...');
                exit;
            } else {
                if(is_callable($callback)){
                    uiLater(function() use ($callback, $return){
                        call_user_func($callback, $return);
                    });
                }
            }
        }))->start();
    }  
}