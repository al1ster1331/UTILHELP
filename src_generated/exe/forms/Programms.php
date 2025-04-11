<?php
namespace exe\forms;

use std, gui, framework, exe;
use action\Element; 


class Programms extends AbstractForm
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
				app()->hideForm('Programms');
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
				app()->hideForm('Programms');
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

		$this->label5->visible = !$this->label5->visible;
		$this->panel19->visible = !$this->panel19->visible;
		$this->label5->x = 288;
		$this->label5->y = 136;
		$this->panel19->x = 280;
		$this->panel19->y = 128;

        
    }

    /**
     * @event panel4.mouseExit 
     */
    function doPanel4MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel19->visible = !$this->panel19->visible;
		$this->label5->visible = !$this->label5->visible;

        
    }

    /**
     * @event panel3.mouseEnter 
     */
    function doPanel3MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel18->visible = !$this->panel18->visible;
		$this->label6->visible = !$this->label6->visible;
		$this->label6->x = 536;
		$this->label6->y = 136;
		$this->panel18->x = 528;
		$this->panel18->y = 128;

        
    }

    /**
     * @event panel3.mouseExit 
     */
    function doPanel3MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel18->visible = !$this->panel18->visible;
		$this->label6->visible = !$this->label6->visible;

        
    }

    /**
     * @event panel5.mouseEnter 
     */
    function doPanel5MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label7->visible = !$this->label7->visible;
		$this->panel20->visible = !$this->panel20->visible;
		$this->label7->x = 784;
		$this->label7->y = 136;
		$this->panel20->x = 776;
		$this->panel20->y = 128;

        
    }

    /**
     * @event panel6.mouseEnter 
     */
    function doPanel6MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label8->visible = !$this->label8->visible;
		$this->panel21->visible = !$this->panel21->visible;
		$this->label8->x = 472;
		$this->label8->y = 136;
		$this->panel21->x = 464;
		$this->panel21->y = 128;

        
    }

    /**
     * @event panel6.mouseExit 
     */
    function doPanel6MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel21->visible = !$this->panel21->visible;
		$this->label8->visible = !$this->label8->visible;

        
    }

    /**
     * @event panel7.mouseEnter 
     */
    function doPanel7MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label9->visible = !$this->label9->visible;
		$this->panel22->visible = !$this->panel22->visible;
		$this->label9->x = 712;
		$this->label9->y = 136;
		$this->panel22->x = 704;
		$this->panel22->y = 128;

        
    }

    /**
     * @event panel8.mouseEnter 
     */
    function doPanel8MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label10->visible = !$this->label10->visible;
		$this->panel23->visible = !$this->panel23->visible;
		$this->label10->x = 288;
		$this->label10->y = 351;
		$this->panel23->x = 280;
		$this->panel23->y = 344;

        
    }

    /**
     * @event panel8.mouseExit 
     */
    function doPanel8MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel23->visible = !$this->panel23->visible;
		$this->label10->visible = !$this->label10->visible;

        
    }

    /**
     * @event panel10.mouseEnter 
     */
    function doPanel10MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label11->visible = !$this->label11->visible;
		$this->panel24->visible = !$this->panel24->visible;
		$this->label11->x = 536;
		$this->label11->y = 352;
		$this->panel24->x = 528;
		$this->panel24->y = 344;

        
    }

    /**
     * @event panel10.mouseExit 
     */
    function doPanel10MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel24->visible = !$this->panel24->visible;
		$this->label11->visible = !$this->label11->visible;

        
    }

    /**
     * @event panel11.mouseEnter 
     */
    function doPanel11MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label12->visible = !$this->label12->visible;
		$this->panel25->visible = !$this->panel25->visible;
		$this->panel25->x = 776;
		$this->panel25->y = 344;
		$this->label12->x = 784;
		$this->label12->y = 352;

        
    }

    /**
     * @event panel5.mouseExit 
     */
    function doPanel5MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel20->visible = !$this->panel20->visible;
		$this->label7->visible = !$this->label7->visible;

        
    }

    /**
     * @event panel7.mouseExit 
     */
    function doPanel7MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel22->visible = !$this->panel22->visible;
		$this->label9->visible = !$this->label9->visible;

        
    }

    /**
     * @event panel11.mouseExit 
     */
    function doPanel11MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->panel25->visible = !$this->panel25->visible;
		$this->label12->visible = !$this->label12->visible;

        
    }

    /**
     * @event panel4.click-Left 
     */
    function doPanel4ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://browser.yandex.ru/download?os=win&bitness=64&statpromo=true&darktheme=1&banerid=6301000000&partner_id=exp_tablo_1&portal_testids=1114258%2F-1%2C1114347%2F-1%2C1124063%2F-1%2C1127618%2F-1%2C1168901%2F16%2C1176504%2F-1%2C1190158%2F97&signature=GW6QlMqLgnc847%2FjQN0%2BZjZTgjPtaT09cc8zRmA3quYIChXMysem0F3AUNBWvNFX%2BcQ2d0oRNgHkyOV6J3Skqw%3D%3D');

        
    }

    /**
     * @event panel3.click-Left 
     */
    function doPanel3ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://www.google.com/chrome/');

        
    }

    /**
     * @event panel5.click-Left 
     */
    function doPanel5ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://www.7-zip.org/');

        
    }

    /**
     * @event panel6.click-Left 
     */
    function doPanel6ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://download.aida64.com/aida64extreme750.exe');

        
    }

    /**
     * @event panel7.click-Left 
     */
    function doPanel7ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://download.msi.com/uti_exe/vga/MSIAfterburnerSetup.zip?__token__=exp=1739732397~acl=/*~hmac=47a1a04d6ac54ce967f172e7a62550a9752752d012afdfe31857d713428b2517');

        
    }

    /**
     * @event panel8.click-Left 
     */
    function doPanel8ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://sourceforge.net/projects/crystaldiskinfo/files/9.5.0/CrystalDiskInfo9_5_0.exe/download');

        
    }

    /**
     * @event panel10.click-Left 
     */
    function doPanel10ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://www.fosshub.com/qBittorrent.html');

        
    }

    /**
     * @event panel11.click-Left 
     */
    function doPanel11ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://github.com/pbatard/rufus/releases/download/v4.6/rufus-4.6.exe');

        
    }

    /**
     * @event panel12.mouseEnter 
     */
    function doPanel12MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label13->visible = !$this->label13->visible;
		$this->panel27->visible = !$this->panel27->visible;
		$this->label13->x = 472;
		$this->label13->y = 352;
		$this->panel27->x = 464;
		$this->panel27->y = 352;

        
    }

    /**
     * @event panel12.mouseExit 
     */
    function doPanel12MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label13->visible = !$this->label13->visible;
		$this->panel27->visible = !$this->panel27->visible;

        
    }

    /**
     * @event panel13.mouseEnter 
     */
    function doPanel13MouseEnter(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label14->visible = !$this->label14->visible;
		$this->panel26->visible = !$this->panel26->visible;
		$this->label14->x = 712;
		$this->label14->y = 356;
		$this->panel26->x = 704;
		$this->panel26->y = 356;

        
    }

    /**
     * @event panel13.mouseExit 
     */
    function doPanel13MouseExit(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->label14->visible = !$this->label14->visible;
		$this->panel26->visible = !$this->panel26->visible;

        
    }

    /**
     * @event panel13.click-Left 
     */
    function doPanel13ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://hdd.by/Victoria/Victoria537.zip');

        
    }

    /**
     * @event panel12.click-Left 
     */
    function doPanel12ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		browse('https://forum.ru-board.com/topic.cgi?forum=5&topic=50519');

        
    }


    /**
     * @event label15.click-Left 
     */
    function doLabel15ClickLeft(UXMouseEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		$this->progressIndicator->show();
		waitAsync(500, function () use ($e, $event) {
			app()->showForm('Launchers');
			waitAsync(100, function () use ($e, $event) {
				app()->hideForm('Programms');
				$this->progressIndicator->hide();
			});
		});

        
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
