##################################################################################################################
#
# Copyright (C) 2014 KTec S.r.l.
#
# Author: Luigi Di Naro: Luigi.DiNaro@KTec.it
# Modified by: Franco Lucchini: flucchini@gmail.com
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################################################

from distutils.core import setup

files = ["xsd/*.xsd"]

setup(
  name = 'PyFePA',
  packages = ['PyFePA'],
  version = '1.2.6',
  description = 'Python object of italian FatturaPA, serialize, deserialize and verify',
  author = 'Franco Lucchini',
  author_email = 'flucchini@gmail.com',
  url = 'https://github.com/franklx/PyFePA',
  download_url = 'https://github.com/franklx/PyFePA/tarball/1.2.6',
  keywords = ['FatturaPA', 'financial', 'utils'],
  platforms= 'OSX, *unix, win',
  package_data = {'PyFePA' : files },
  license= 'AGPLv3',
  classifiers = [],
  install_requires=[],
)
