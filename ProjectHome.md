# Intrinsec Android SSL Patch #

## Summary ##

This program can be used during mobile application assessment or mobile malware on android platform to patch the binary application (APK file) in order to disable SSL certificates verifications.

The application communications can be analyzed through an interception proxy (Burp, RAT, Webscarab,etc.)

This program is not intented for any other use.

This program follow theses steps:
  1. Application decompilation
  1. Add required file to circumvent SSL verification
  1. Parse source code to identify HTTPS connections establishment and patch the code
  1. Application compilation
  1. Add the original ressources (images, layouts, etc.)

It relies on use of [APKTool](http://code.google.com/p/android-apktool/) and [Smali](http://code.google.com/p/smali/).
It implements a method described by [Foundstone](https://secure.mcafee.com/us/resources/white-papers/wp-defeating-ssl-cert-validation.pdf)


## History ##

The tool has been developped during research and development around a mobile application assessment methodology performed by Intrinsec during penetration testing, security audits and forensic.

The tool has been developped by Marc Lebrun (marc.lebrun@intrinsec.com), supported by Guillaume Lopes (guillaumes.lopes@intrinsec.com)

## Usage ##
```
user$ ./intrinsec-android-ssl-patch <apk-file>
```
## Links ##
  * http://securite.intrinsec.com/fr/2011/07/android-et-ssl.html#more (FRENCH ARTICLE)
  * http://www.intrinsec.com
  * http://securite.intrinsec.com
  * Twitter : [@infsec](http://twitter.com/#!/infsec)