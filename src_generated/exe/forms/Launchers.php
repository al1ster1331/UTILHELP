<?php
namespace exe\forms;

use std, gui, framework, exe;
use action\Element; 


class Launchers extends AbstractForm
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
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->progressIndicator->show();
		waitAsync(500, function () use ($e, $event) {
			app()->showForm('Drivers');
			waitAsync(100, function () use ($e, $event) {
				app()->hideForm('Launchers');
				$this->progressIndicator->hide();
			});
		});

        
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
				app()->hideForm('Launchers');
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
				app()->hideForm('Launchers');
				$this->progressIndicator->hide();
			});
		});

        
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

		browse('https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe');

        
    }

    /**
     * @event panel6.click-Left 
     */
    function doPanel6ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://media.contentapi.ea.com/content/dam/eacom/ea-app/common/ea-app-cta-windows.png.adapt.crop16x9.652w.png');

        
    }

    /**
     * @event panel7.click-Left 
     */
    function doPanel7ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://downloader.battle.net//download/getInstallerForGame?os=win&gameProgram=BATTLENET_APP&version=Live');

        
    }

    /**
     * @event panel8.click-Left 
     */
    function doPanel8ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://ubi.li/4vxt9');

        
    }

    /**
     * @event panel9.click-Left 
     */
    function doPanel9ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi?trackingId=b9a2eb47d1824fc9b7a976355939bd2d');

        
    }

    /**
     * @event panel3.click-Left 
     */
    function doPanel3ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://github.com/hydralauncher/hydra/releases/download/v3.4.0/hydralauncher-3.4.0-setup.exe');

        
    }


    /**
     * @event label11.click-Left 
     */
    function doLabel11ClickLeft(UXMouseEvent $e = null)
    {    
        
    }

    /**
     * @event label27.click-Left 
     */
    function doLabel27ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		app()->showFormAndWait('Info');

        
    }

    /**
     * @event label28.click-Left 
     */
    function doLabel28ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		app()->showFormAndWait('contacts');

        
    }

    /**
     * @event label29.click-Left 
     */
    function doLabel29ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->toast('В стадии разработки.');

        
    }






















}
