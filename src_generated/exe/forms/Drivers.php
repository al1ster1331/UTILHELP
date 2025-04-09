<?php
namespace exe\forms;

use std, gui, framework, exe;
use action\Element; 


class Drivers extends AbstractForm
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
     * @event label3.click-Left 
     */
    function doLabel3ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event labelAlt.click-Left 
     */
    function doLabelAltClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->progressIndicator->show();
		waitAsync(500, function () use ($e, $event) {
			app()->showForm('MainForm');
			waitAsync(100, function () use ($e, $event) {
				app()->hideForm('Drivers');
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
				app()->hideForm('Drivers');
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
     * @event panel4.mouseEnter 
     */
    function doPanel4MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label5->x = 288;
		$this->label5->y = 136;
		$this->panel18->x = 280;
		$this->panel18->y = 128;
		$this->panel18->visible = !$this->panel18->visible;
		$this->label5->visible = !$this->label5->visible;

        
    }

    /**
     * @event panel4.mouseExit 
     */
    function doPanel4MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label5->visible = !$this->label5->visible;
		$this->panel18->visible = !$this->panel18->visible;

        
    }

    /**
     * @event panel6.mouseEnter 
     */
    function doPanel6MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label6->y = 136;
		$this->label6->x = 536;
		$this->panel19->y = 128;
		$this->panel19->x = 528;
		$this->panel19->visible = !$this->panel19->visible;
		$this->label6->visible = !$this->label6->visible;

        
    }

    /**
     * @event panel6.mouseExit 
     */
    function doPanel6MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label6->visible = !$this->label6->visible;
		$this->panel19->visible = !$this->panel19->visible;

        
    }

    /**
     * @event panel7.mouseEnter 
     */
    function doPanel7MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label7->y = 136;
		$this->label7->x = 784;
		$this->panel20->y = 128;
		$this->panel20->x = 776;
		$this->panel20->visible = !$this->panel20->visible;
		$this->label7->visible = !$this->label7->visible;

        
    }

    /**
     * @event panel7.mouseExit 
     */
    function doPanel7MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label7->visible = !$this->label7->visible;
		$this->panel20->visible = !$this->panel20->visible;

        
    }

    /**
     * @event panel8.mouseEnter 
     */
    function doPanel8MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label8->x = 465;
		$this->label8->y = 136;
		$this->panel21->x = 456;
		$this->panel21->y = 128;
		$this->label8->visible = !$this->label8->visible;
		$this->panel21->visible = !$this->panel21->visible;

        
    }

    /**
     * @event panel8.mouseExit 
     */
    function doPanel8MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label8->visible = !$this->label8->visible;
		$this->panel21->visible = !$this->panel21->visible;

        
    }

    /**
     * @event panel9.mouseEnter 
     */
    function doPanel9MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label9->x = 708;
		$this->label9->y = 136;
		$this->panel22->x = 704;
		$this->panel22->y = 128;
		$this->panel22->visible = !$this->panel22->visible;
		$this->label9->visible = !$this->label9->visible;

        
    }

    /**
     * @event panel9.mouseExit 
     */
    function doPanel9MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel22->visible = !$this->panel22->visible;
		$this->label9->visible = !$this->label9->visible;

        
    }

    /**
     * @event panel3.mouseEnter 
     */
    function doPanel3MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label10->x = 290;
		$this->label10->y = 351;
		$this->panel23->x = 280;
		$this->panel23->y = 344;
		$this->panel23->visible = !$this->panel23->visible;
		$this->label10->visible = !$this->label10->visible;

        
    }

    /**
     * @event panel3.mouseExit 
     */
    function doPanel3MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel23->visible = !$this->panel23->visible;
		$this->label10->visible = !$this->label10->visible;

        
    }

    /**
     * @event panel4.click-Left 
     */
    function doPanel4ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://www.amd.com/en/support/download/drivers.html');

        
    }

    /**
     * @event panel6.click-Left 
     */
    function doPanel6ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://www.nvidia.com/en-us/drivers/');

        
    }

    /**
     * @event panel7.click-Left 
     */
    function doPanel7ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://github.com/abbodi1406/vcredist/releases');

        
    }

    /**
     * @event panel8.click-Left 
     */
    function doPanel8ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://download.microsoft.com/download/7/0/3/703455ee-a747-4cc8-bd3e-98a615c3aedb/dotNetFx35setup.exe');

        
    }

    /**
     * @event panel9.click-Left 
     */
    function doPanel9ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://javadl.oracle.com/webapps/download/AutoDL?BundleId=251656_7ed26d28139143f38c58992680c214a5');

        
    }

    /**
     * @event panel3.click-Left 
     */
    function doPanel3ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://www.realtek.com/Download/List?cate_id=593&menu_id=298');

        
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
     * @event label11.click-Left 
     */
    function doLabel11ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->progressIndicator->show();
		waitAsync(500, function () use ($e, $event) {
			app()->showForm('Launchers');
			waitAsync(100, function () use ($e, $event) {
				app()->hideForm('Drivers');
				$this->progressIndicator->hide();
			});
		});

        
    }






















}
