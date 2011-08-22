#!/usr/bin/env python
#
# Copyright (c) 2011 by Intrinsec
# http://www.intrinsec.com
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# Please visit http://securite.intrinsec.com/fr/blog/ for more informations or
# if want to post comments.
#

import os
import sys
import zipfile
import zlib
import shutil
import errno
import distutils.dir_util
import re

apktool = "./apktool.jar"
smalidir = "./smali/"

def usage():
    print "usage : ./ssl-patch <apk file>"

def unzip_apk(infile, output):
    zfile = zipfile.ZipFile(infile, 'r')
    zfile.extractall(output)
    zfile.close()

def zip_to_apk(indir, output):
    outapk = zipfile.ZipFile(output, 'w')
    for (path, dirs, files) in os.walk(indir):
        zipath = path[len("./" + output):]
        for filename in files:
            outapk.write(os.path.join(path, filename), os.path.join(zipath, filename), zipfile.ZIP_DEFLATED)
    outapk.close()

def escape_dollar(string):
    return(re.sub('\$','\\$',string))

if (len(sys.argv) != 2):
    usage()
    exit()

apk = sys.argv[1]
outdir = "./" + apk + "-dir" 
zipdir = "./" + apk + "-zip" 

unzip_apk(apk, zipdir)

print "Decompression of " + apk + " done."

os.system("java -jar " + apktool + " d " + apk + " " + outdir)
print "Decompilation of " + apk + " done."

try:
    os.makedirs(outdir + "/smali/com/android")
except OSError as exc:
    if exc.errno == errno.EEXIST:
        pass
    else: raise

print "Patching smali files..."
for (path, dirs, files) in os.walk(outdir + "/smali/"):
    for smalifile in files:
        filename, ext = os.path.splitext(smalifile)
        if ext == ".smali":
            os.system("sed -i 's/org\/apache\/http\/impl\/client\/DefaultHttpClient/com\/android\/MyHttpClient/g' " + escape_dollar(os.path.join(path, smalifile)))
            os.system("sed -i 's/check-cast v\([0-9]\+\), Ljavax\/net\/ssl\/HttpsURLConnection;/invoke-static \{\}, Lcom\/android\/httpsurlbypass;->trustAllHosts()V\\n    &/g' " + escape_dollar(os.path.join(path, smalifile)))
            os.system("sed -i 's/check-cast v\([0-9]\+\), Ljavax\/net\/ssl\/HttpsURLConnection;/&\\n    invoke-static \{v\\1\}, Lcom\/android\/bypass;->httpsurlconnectionbypass(Ljavax\/net\/ssl\/HttpsURLConnection;)V/g' " + escape_dollar(os.path.join(path, smalifile)))
            os.system("sed -i 's/invoke-virtual {v\([0-9]\+\), v1}, Landroid\/webkit\/WebView;->loadUrl(Ljava\/lang\/String;)V/invoke-static \{v\\1\}, Lcom\/android\/bypass1;->webviewbypass(Landroid\/webkit\/WebView;)V\\n    &/g' " + escape_dollar(os.path.join(path, smalifile)))
print "All files patched."

smalilist = os.listdir(smalidir)
for smalifile in smalilist:
    shutil.copy(smalidir + smalifile, outdir + "/smali/com/android/")
print "Smali code included."

apkname, ext = os.path.splitext(apk)
newapk = apkname + "-new" + ext
os.system("java -jar " + apktool + " b " + outdir + " " + newapk)
print "Recompilation of " + newapk + " done."

shutil.rmtree(outdir)

unzip_apk(newapk, outdir)

distutils.dir_util.copy_tree(zipdir + "/res/", outdir + "/res/")

shutil.rmtree(zipdir)
os.remove(newapk)

zip_to_apk(outdir, newapk)
print "Resources re-added, for compatibility."

shutil.rmtree(outdir)
