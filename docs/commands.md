# COMANDOS

Podemos ver todas las opciones del programa escribiendo el comando **sdkcpc** seguido del argumento correspondiente y de la opción en el caso de que la tubiera.

```
sdkcpc [argumento] [opcion]
```

Ejemplo
```
$ sdkcpc -h

sdkcpc v1.0.1
linux -  Build: 2022/09/04 11:17:00

© Destroyer 2022

usage: sdkcpc [-h] [-v] {about,make,deploy,validate,info,new,new-8bp,run} ...

positional arguments:
  {about,make,deploy,validate,info,new,new-8bp,run}
                        commands
    about               Shows information about Basic SDK
    make                make the DSK image of the project
    deploy              Make and Run the dsk image on the emulator or M4-Board
    validate            Project data validation.
    info                Show information of project
    new                 Create new basic project
    new-8bp             Create new basic project 8bp
    run                 Run BAS File in DSK image

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```


### about

Muestra información del desarrollador del proyecto.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc about`    |     | Muestra información del software y del desarrollador    |

### -h, --help

Muestra información del desarrollador del proyecto.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc about`    |     | Muestra información del software y del desarrollador    |



### info

Muestra información del proyecto de la ruta actual.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc info`    |    | Muestra información del proyecto de la ruta actual.|

### make

Crea una imagen para Disco (DSK) y Cinta (CDT) con el software del proyecto


| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc make`    |     | Genera un archivo DSK con todo el software del proyecto.    |

### new

Crea un nuevo proyecto en la ruta actual con la estructura necesaria para empezar.
El argumento lleva como opción el nombre que asignaremos a nuestro proyecto.

```
sdkcpc new [Nombre_proyecto]
```
> 
> **El Nombre de proyecto no admite espacios.**

```
$ sdkcpc new mibas                                                                          
sdkcpc v1.0.2
linux - Build: 2022/09/10 12:14:17

© Destroyer 2022

[*] ------------------------------------------------------------------------
[*] Create New Project mibas
[*] ------------------------------------------------------------------------
[+] Create Folder mibas/resources
[+] Create Folder mibas/ascii
[+] Create Folder mibas/bin
[+] Create Folder mibas/src
[+] Create Folder mibas/obj
[+] Create Template /home/destroyer/Documentos/Github/SDKCPC/cpc/pepep/mibas/Project.cfg
[+] Create Template /home/destroyer/Documentos/Github/SDKCPC/cpc/pepep/mibas/src/mibas.bas
[?] Do you want to create version control in the project (git software needed)?: No
   Yes
 > No

[?] Do you want to open the new Project with Visual Studio Code?: Yes
 > Yes
   No

[+] Create Vscode files.
[*] ------------------------------------------------------------------------
[*] mibas project successfully created
[*] ------------------------------------------------------------------------
```

### new-8bp

Crea un nuevo proyecto en la ruta actual con la estructura necesaria para trabajar con la libreria  [8BP](https://github.com/jjaranda13/8BP)

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc new-8bp`    | [Nombre_proyecto]  |El argumento lleva como opción el nombre que asignaremos a nuestro proyecto.|

> **NOTA:** 
> **No se admiten espacios en el nombre del proyecto.**
---

### run

Carga nuestro DSK generado y ejecuta el bas seleccionado sobre el emulador pasado como opcion al argumento.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc run`    |  --rvm   | Ejecuta el emulador Retro virtual Machine.|
---

### deploy

Carga nuestro DSK generado y ejecuta el bas seleccionado sobre el emulador pasado como opcion al argumento.

| Como Usar  | Opciones  | Descripcion  |
|:----------|:----------|:----------|
| `sdkcpc deploy`    |  --rvm   | Compila y carga el dsk resultante en el emulador Retro virtual Machine.|

### -v, --version

Muestra la version del software actual.

```shell
$ sdkcpc --version                  

sdkcpc v1.0.1
linux -  Build: 2022/09/04 11:17:00

© Destroyer 2022
```

### validate

Valida que las configuraciones del proyecto en la ruta actual esten correctas.

```shell
$ sdkcpc validate     

sdkcpc v1.0.2
linux - Build: 2022/09/10 12:14:17

© Destroyer 2022

[*] ------------------------------------------------------------------------
[*] Project.cfg Successfull
[*] ------------------------------------------------------------------------

```
#### -v, --verbose 

Muestra toda la información del proceso de validación.

```shell
$ sdkcpc validate --verbose  

sdkcpc v1.0.2
linux - Build: 2022/09/10 12:14:17

© Destroyer 2022

[*] ------------------------------------------------------------------------
[*] Project.cfg
[*] ------------------------------------------------------------------------
[*] COMPILATION 
[*]   compilation: 2022-11-11 12:08:16.320710 [OK]
[*]   version: 0.0.1 [OK]
[*] GENERAL 
[*]   name: mibas [OK]
[*]   description: None [OK]
[*]   template: BASIC [OK]
[*]   authors: authors <authors@mail.com> [OK]
[*] CONFIG 
[*]   concatenate.bas.files: No [OK]
[*]   name.bas.file: mibas.bas [OK]
[*] RETRO VIRTUAL MACHINE 
[*]   model.cpc: 6128 [OK]
[*] M4 BOARD 
[*]   ip: 0.0.0.0 [OK]
[*] ------------------------------------------------------------------------
[*] Project.cfg Successfull
[*] ------------------------------------------------------------------------

```