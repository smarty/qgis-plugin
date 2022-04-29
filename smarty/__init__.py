# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Smarty
                                 A QGIS plugin
 Smarty attempt
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-01-19
        copyright            : (C) 2022 by Smarty
        email                : osgeo-it@smarty.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
import subprocess
import sys
import platform

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Smarty class from file Smarty.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    # x = str(sys.executable) 
    currentPlatform = platform.system()

    if len(currentPlatform) == 0:
        return

    if currentPlatform == 'Windows':

        subprocess.check_call(["attrib", "-r", 'C:/Program Files/QGIS 3.24.2/apps/Python39/Lib/site-packages'])

        # TODO: Find path to the site-packages place
        # TODO: Find how to change permissions for 'Windows'
        # TODO: Find path to the python executable

        process = subprocess.Popen(['C:/Program Files/QGIS 3.24.2/bin/python.exe','-m','pip', 'install', '--verbose', '--trusted-host=pypi.org','--trusted-host=pypi.python.org','--trusted-host=files.pythonhosted.org', 'smartystreets_python_sdk'], stdout=subprocess.PIPE)
    elif currentPlatform == 'Linux' | currentPlatform == 'Darwin':
        # TODO: Find path to the site-packages place
        # TODO: Find how to change permissions for 'Darwin'/'Linux'
        # TODO: Find path to the python executable

        subprocess.run(['chmod', '0444', 'C:/Program Files/QGIS 3.24.2/apps/Python39/Lib/site-packages'])

        process = subprocess.Popen(['C:/Program Files/QGIS 3.24.2/bin/python.exe','-m','pip', 'install', '--verbose', '--trusted-host=pypi.org','--trusted-host=pypi.python.org','--trusted-host=files.pythonhosted.org', 'smartystreets_python_sdk'], stdout=subprocess.PIPE)
    else:
        return
    
    
    # process = subprocess.Popen([x,  '-m', 'pip', 'install', '--verbose', '--trusted-host=pypi.org','--trusted-host=pypi.python.org','--trusted-host=files.pythonhosted.org','smartystreets_python_sdk'], stdout=subprocess.PIPE)
    # process = subprocess.Popen(["c:/Program Files/QGIS 3.24.2/apps/Python39/python3.exe",  '-m', 'pip', 'install', 'smartystreets_python_sdk'], stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    x = str('STDOUT:{}'.format(stdout))
    print(x)
    
    from .smarty import Smarty

    return Smarty(iface)


