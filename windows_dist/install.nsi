#==============================
# Includes
#!include "WinMessages.nsh"
#!include UpgradeDLL.nsh
!include "MUI.nsh"

#=============================================================================
# Optionen
name "Medienverwaltung"
OutFile "Install_Medienverwaltung.exe"
#InstallDir "$PROGRAMFILES\Medienverwaltung"
InstallDir "$APPDATA\Medienverwaltung"
!ifdef DEBUG
    SetCompressor zlib
    SetCompress off
!else
    SetCompressor /SOLID lzma
!endif

#=============================================================================
# Globale Variablen
Var STARTMENU_FOLDER

#=============================================================================
# Pages

;WelcomePage
!define MUI_COMPONENTSPAGE_NODESC
!insertmacro MUI_PAGE_WELCOME

;Zielverzeichnis
#InstallDirRegKey HKLM Software\sis\Medienverwaltung InstallLocation
!insertmacro MUI_PAGE_DIRECTORY

;Was soll installiert werden?
#!insertmacro MUI_PAGE_COMPONENTS

;Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "Medienverwaltung"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKLM"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Medienverwaltung"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
!insertmacro MUI_PAGE_STARTMENU Application $STARTMENU_FOLDER

!insertmacro MUI_PAGE_INSTFILES
ShowInstDetails show

!define MUI_FINISHPAGE_RUN "$INSTDIR\start.cmd"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!insertmacro MUI_PAGE_FINISH

#=============================================================================
# UnInstallPages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_COMPONENTS
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "German"

#=============================================================================
#!macro InstExe SourceDir Filename
#  DetailPrint "InstExe('${SourceDir}', '${Filename}', '$INSTDIR')"
#  File "${SourceDir}\${Filename}"
#  ExecWait "$INSTDIR\${Filename} /regserver"
#  DetailPrint "$INSTDIR\${Filename}"
#!macroend


Function .onInit
    #==============================
    # AdminCheck - Anfang
    ClearErrors
    UserInfo::GetName
    IfErrors Win9x
    Pop $0
    UserInfo::GetAccountType
    Pop $1
    StrCmp $1 "Admin" 0 +2
    Goto done

    MessageBox MB_OK|MB_ICONSTOP "Der Benutzer '$0' ist hat keine administrativen Rechte. Das Setup wird beendet."
    abort

    Win9x:
    # This one means you don't need to care about admin or
    # not admin because Windows 9x doesn't either
    MessageBox MB_OK|MB_ICONSTOP "Diese Programm ist nicht unter Windows 9x lauff�hig. Das Setup wird beendet."
    abort

    done:
    #    AdminCheck - Ende
    #==============================
FunctionEnd

Function .onInstSuccess
    WriteUninstaller $INSTDIR\Uninstall.exe

    ;Create shortcuts
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    !insertmacro MUI_STARTMENU_WRITE_END
    
    WriteRegStr HKLM Software\sis\Medienverwaltung InstallLocation $INSTDIR

    IfRebootFlag 0 noreboot
        MessageBox MB_YESNO "A reboot is required to finish the installation. Do you wish to reboot now?" IDNO noreboot
        Reboot
    noreboot:
FunctionEnd

Function checkRetVal
    Pop $0
    ${If} $0 != 0
        MessageBox MB_OK|MB_ICONSTOP "InstallUtil returned: $0"
        DetailPrint "InstallUtil returned: $0"
    ${EndIf}
FunctionEnd

#Function un.checkRetVal
#    Pop $0
#    ${If} $0 != 0
#        MessageBox MB_OK|MB_ICONSTOP "InstallUtil returned: $0"
#        DetailPrint "InstallUtil returned: $0"
#    ${EndIf}
#FunctionEnd

Section "Python26"
    SetOutPath $INSTDIR
    File /r /x Doc /x tcl /x test C:\Python26
    File python26.dll
    File install.cmd
    File show.cmd
    File start.cmd
    
    DetailPrint "Downloading and installing runtime environment"
    AddSize 30000
    nsExec::ExecToLog /OEM '"$INSTDIR\install.cmd"'
    call checkRetVal

    ;Create shortcuts
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Start Webserver.lnk" "$INSTDIR\start.cmd"
#    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Edit config.lnk" "$INSTDIR\production.ini"
    !insertmacro MUI_STARTMENU_WRITE_END
    
#        File "..\Medienverwaltung.exe"
#        File "..\*.metaDatatypes"
#        File "..\*.SnapshotProperties"


SectionEnd

Section /o "Un.Database"
    Delete $INSTDIR\production.db
SectionEnd

Section "-Un.Remove_What_is_Left"
    ReadRegStr $STARTMENU_FOLDER HKLM "Software\Medienverwaltung" "Start Menu Folder"
    Delete "$SMPROGRAMS\$STARTMENU_FOLDER\Start Webserver.lnk"
    Delete "$SMPROGRAMS\$STARTMENU_FOLDER\Uninstall.lnk"
    RMDir "$SMPROGRAMS\$STARTMENU_FOLDER"
    DeleteRegKey HKLM "Software\Medienverwaltung"

    Delete $INSTDIR\python26.dll
    Delete $INSTDIR\install.cmd
    Delete $INSTDIR\show.cmd
    Delete $INSTDIR\start.cmd
    Delete $INSTDIR\manage_local.py
    Delete $INSTDIR\production.ini
    Delete $INSTDIR\Uninstall.exe
    RMDir /r $INSTDIR\Python26
    RMDir /r $INSTDIR\local.env
    RMDir /r $INSTDIR\Data
    RMDir $INSTDIR
SectionEnd
