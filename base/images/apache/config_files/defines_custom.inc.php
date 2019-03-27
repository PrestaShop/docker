<?php
/**
 * 2007-2019 PrestaShop and Contributors
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Open Software License (OSL 3.0)
 * that is bundled with this package in the file LICENSE.txt.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/OSL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://www.prestashop.com for more information.
 *
 * @author    PrestaShop SA <contact@prestashop.com>
 * @copyright 2007-2019 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/OSL-3.0 Open Software License (OSL 3.0)
 * International Registered Trademark & Property of PrestaShop SA
 */
if ((bool) getenv('PS_DEV_MODE')) {
    define('_PS_MODE_DEV_', (bool) getenv('PS_DEV_MODE'));
}
if ((bool) getenv('PS_DEMO_MODE')) {
    define('_PS_MODE_DEMO_', (bool) getenv('PS_DEMO_MODE'));
}
// FYI: Defining env var _PS_HOST_MODE_ as true also works natively
if ((bool) getenv('PS_HOST_MODE')) {
    define('_PS_HOST_MODE_', (bool) getenv('PS_HOST_MODE'));
}
