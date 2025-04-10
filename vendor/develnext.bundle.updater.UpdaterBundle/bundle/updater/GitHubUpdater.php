<?php
namespace bundle\updater;

use php\lang\Thread;
use bundle\updater\AbstractUpdater;

/**
 * Загрузка обновлений из репозитория GitHub 
 * (из раздела releases)
 */
class GitHubUpdater extends AbstractUpdater {
    /**
     * Имя пользователя на GitHub
     * @var string
     */
    protected $user;
    
    /**
     * Название репозитория
     * @var string
     */
    protected $repo;
    
    /**
     * Хранение данных о последнем релизе
     * @var array
     */
    protected $lastRelease = [];
    
    public function __construct($user, $repo){
        $this->user = $user;    
        $this->repo = $repo;    
    }
    
    /**
     * Получить последний релиз 
     */
    protected function getLastRelease() {
        $url = 'https://api.github.com/repos/'.$this->user.'/'.$this->repo.'/releases/latest';
        $data = json_decode(file_get_contents($url), true);
        if(is_array($data) && isset($data['assets'][0])){
            $this->lastRelease = [
                'version' => $data['tag_name'],
                'description' => $data['body'],
                'url' => $data['assets'][0]['browser_download_url'],
                'size' => $data['assets'][0]['size'],
                'name' => $data['assets'][0]['name'],
            ];
        }
    }
    
    /**
     * Проверка на наличие обновлений
     * @param callable $callback Первый аргумент true если необходимо обновление 
     * @async
     */
    public function checkUpdates(callable $callback){
        (new Thread(function() use ($callback){
            $this->getLastRelease();
            uiLater(function() use ($callback){
                $update = isset($this->lastRelease['version']) && $this->compareVersion($this->lastRelease['version']);
                call_user_func($callback, $update, $this->lastRelease);
            });
        }))->start();
    }
    
    /**
     * Установка последнего обновления
     * @param callable $progress см. AbstractUpdater->applyUpdate
     */
    public function installUpdate(callable $progress){
        if(isset($this->lastRelease['version']) && isset($this->lastRelease['url'])){
            parent::applyUpdate($this->lastRelease['url'], $this->lastRelease['name'], $this->lastRelease['size'], $progress);
        }
    }
}
