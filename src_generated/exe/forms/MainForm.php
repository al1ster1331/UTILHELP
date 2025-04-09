<?php
namespace exe\forms;

use std, gui, framework, exe;
use bundle\updater\AbstractUpdater;
use bundle\updater\UpdateMe;
use bundle\updater\GitHubUpdater;
use action\Element; 



class MainForm extends AbstractForm
{

    /**
     * @event imageAlt.click-Left 
     */
    function doImageAltClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		app()->minimizeForm($this->getContextFormName());

        
    }

    /**
     * @event image.click-Left 
     */
    function doImageClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		app()->shutdown();

        
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
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->progressIndicator->show();
		waitAsync(500, function () use ($e, $event) {
			app()->showForm('Drivers');
			waitAsync(100, function () use ($e, $event) {
				app()->hideForm('MainForm');
				$this->progressIndicator->hide();
			});
		});

        
    }

    /**
     * @event label4.click-Left 
     */
    function doLabel4ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->progressIndicator->show();
		waitAsync(500, function () use ($e, $event) {
			app()->showForm('Programms');
			waitAsync(100, function () use ($e, $event) {
				app()->hideForm('MainForm');
				$this->progressIndicator->hide();
			});
		});

        
    }





    /**
     * @event image39.click-Left 
     */
    function doImage39ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://github.com/al1ster1331/UTILHELP');

        
    }

    /**
     * @event image40.click-Left 
     */
    function doImage40ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://t.me/UTILHELP13');

        
    }

    /**
     * @event label7.mouseEnter 
     */
    function doLabel7MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel5->glowEffect->enable();

        
    }

    /**
     * @event label7.mouseExit 
     */
    function doLabel7MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel5->glowEffect->disable();

        
    }

    /**
     * @event label9.mouseEnter 
     */
    function doLabel9MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel6->glowEffect->enable();

        
    }

    /**
     * @event label9.mouseExit 
     */
    function doLabel9MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel6->glowEffect->disable();

        
    }

    /**
     * @event image5.click-Left 
     */
    function doImage5ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label11->hide();
		$this->label12->hide();
		$this->image5->hide();
		$this->separator5->hide();
		$this->label10->hide();
		$this->panel3->hide();
		$this->panel7->hide();
		$this->panel4->hide();

        
    }

    /**
     * @event panel6.click-Left 
     */
    function doPanel6ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->image5->show();
		$this->separator5->show();
		$this->label12->show();
		$this->label11->show();
		$this->panel7->show();
		$this->label10->show();
		$this->panel3->show();
		$this->panel4->show();
		$this->image5->x = 1120;
		$this->image5->y = 144;
		$this->separator5->x = 111;
		$this->separator5->y = 187;
		$this->label12->x = 120;
		$this->label12->y = 144;
		$this->label11->x = 120;
		$this->label11->y = 160;
		$this->panel7->x = 111;
		$this->panel7->y = 136;
		$this->label10->x = 136;
		$this->label10->y = 200;
		$this->panel3->x = 111;
		$this->panel3->y = 136;
		$this->panel4->x = 0;
		$this->panel4->y = 0;

        
    }
    

    /**
     * @event panel5.click-Left 
     */
    function doPanel5ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->image6->show();
		$this->separator5->show();
		$this->label13->show();
		$this->label14->show();
		$this->panel7->show();
		$this->label15->show();
		$this->panel3->show();
		$this->panel4->show();
		$this->image6->x = 1120;
		$this->image6->y = 144;
		$this->separator5->x = 111;
		$this->separator5->y = 187;
		$this->label13->x = 120;
		$this->label13->y = 144;
		$this->label14->x = 120;
		$this->label14->y = 160;
		$this->panel7->x = 111;
		$this->panel7->y = 136;
		$this->label15->x = 136;
		$this->label15->y = 230;
		$this->panel3->x = 111;
		$this->panel3->y = 136;
		$this->panel4->x = 0;
		$this->panel4->y = 0;

        
    }

    /**
     * @event image6.click-Left 
     */
    function doImage6ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label14->hide();
		$this->label13->hide();
		$this->image6->hide();
		$this->separator5->hide();
		$this->label15->hide();
		$this->panel3->hide();
		$this->panel7->hide();
		$this->panel4->hide();

        
    }

    /**
     * @event label.mouseEnter 
     */
    function doLabelMouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->toast('Версия программы 0.4');

        
    }

    /**
     * @event panel9.click-Left 
     */
    function doPanel9ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->image8->show();
		$this->separator5->show();
		$this->label18->show();
		$this->label19->show();
		$this->panel7->show();
		$this->label20->show();
		$this->panel3->show();
		$this->panel4->show();
		$this->image8->x = 1120;
		$this->image8->y = 144;
		$this->separator5->x = 111;
		$this->separator5->y = 187;
		$this->label19->x = 120;
		$this->label19->y = 144;
		$this->label18->x = 120;
		$this->label18->y = 160;
		$this->panel7->x = 111;
		$this->panel7->y = 136;
		$this->label20->x = 136;
		$this->label20->y = 230;
		$this->panel3->x = 111;
		$this->panel3->y = 136;
		$this->panel4->x = 0;
		$this->panel4->y = 0;

        
    }



    /**
     * @event image8.click-Left 
     */
    function doImage8ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label18->hide();
		$this->label19->hide();
		$this->image8->hide();
		$this->separator5->hide();
		$this->label20->hide();
		$this->panel3->hide();
		$this->panel7->hide();
		$this->panel4->hide();

        
    }

    /**
     * @event label21.mouseEnter 
     */
    function doLabel21MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel9->glowEffect->enable();

        
    }

    /**
     * @event label21.mouseExit 
     */
    function doLabel21MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel9->glowEffect->disable();

        
    }

    /**
     * @event label17.click-Left 
     */
    function doLabel17ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->progressIndicator->show();
		waitAsync(500, function () use ($e, $event) {
			app()->showForm('Launchers');
			waitAsync(100, function () use ($e, $event) {
				app()->hideForm('MainForm');
				$this->progressIndicator->hide();
			});
		});

        
    }









}
