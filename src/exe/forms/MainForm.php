<?php
namespace exe\forms;

use std, gui, framework, exe;
use bundle\updater\AbstractUpdater;
use bundle\updater\UpdateMe;
use bundle\updater\GitHubUpdater;



class MainForm extends AbstractForm
{

    /**
     * @event imageAlt.click-Left 
     */
    function doImageAltClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event image.click-Left 
     */
    function doImageClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event labelAlt.mouseEnter 
     */
    function doLabelAltMouseEnter(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label3.click-Left 
     */
    function doLabel3ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label4.click-Left 
     */
    function doLabel4ClickLeft(UXMouseEvent $e = null)
    {    
        
    }





    /**
     * @event image39.click-Left 
     */
    function doImage39ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event image40.click-Left 
     */
    function doImage40ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label7.mouseEnter 
     */
    function doLabel7MouseEnter(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label7.mouseExit 
     */
    function doLabel7MouseExit(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label9.mouseEnter 
     */
    function doLabel9MouseEnter(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label9.mouseExit 
     */
    function doLabel9MouseExit(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event image5.click-Left 
     */
    function doImage5ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event panel6.click-Left 
     */
    function doPanel6ClickLeft(UXMouseEvent $e = null)
    {    
        
    }
    

    /**
     * Текущая версия программы 
     */
    const VERSION = '0.2';
 
    
    /**
     * @event show 
     */
    function doShow(UXWindowEvent $e = null)
    {    
        // Проверка обновлений
        // Обязательно нужно передать текущую версию программы
        UpdateMe::start(self::VERSION);
    }

    /**
     * @event panel5.click-Left 
     */
    function doPanel5ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event image6.click-Left 
     */
    function doImage6ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label.mouseEnter 
     */
    function doLabelMouseEnter(UXMouseEvent $e = null)
    {    
        
    }

}
