<?php
namespace exe\forms;

use bundle\updater\UpdateMe;
use std, gui, framework, exe;



class Loading extends AbstractForm
{

    /**
     * @event progressBar.construct 
     */
    function doProgressBarConstruct(UXEvent $e = null)
    {    
        
    }

    /**
     * @event progressBarAlt.construct 
     */
    function doProgressBarAltConstruct(UXEvent $e = null)
    {    
        
    }

    /**
     * @event progressBar3.construct 
     */
    function doProgressBar3Construct(UXEvent $e = null)
    {    
        
    }

    /**
     * @event progressBar4.construct 
     */
    function doProgressBar4Construct(UXEvent $e = null)
    {    
$e = $event ?: $e; // legacy code from 16 rc-2

		waitAsync(500, function () use ($e, $event) {
			$this->progressBarAlt->show();
			$this->progressBar->hide();
			waitAsync(750, function () use ($e, $event) {
				$this->progressBar3->show();
				$this->progressBarAlt->hide();
				waitAsync(500, function () use ($e, $event) {
					$this->progressBar3->hide();
					$this->progressBar4->show();
					waitAsync(1000, function () use ($e, $event) {
						$this->loadForm('MainForm');
					});
				});
			});
		});

        
    }


}
