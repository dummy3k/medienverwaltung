#==============================
# Includes
#!include "WinMessages.nsh"
#!include UpgradeDLL.nsh
!include "MUI.nsh"

#=============================================================================
# Optionen
name "Medienverwaltung"
OutFile "Install_Medienverwaltung.exe"
InstallDir "$PROGRAMFILES\Medienverwaltung"
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
InstallDirRegKey HKLM Software\sis\Medienverwaltung InstallLocation
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
    MessageBox MB_OK|MB_ICONSTOP "Diese Programm ist nicht unter Windows 9x lauffähig. Das Setup wird beendet."
    abort

    done:
    #    AdminCheck - Ende
    #==============================
FunctionEnd

Function .onInstSuccess
  IfRebootFlag 0 noreboot
    MessageBox MB_YESNO "A reboot is required to finish the installation. Do you wish to reboot now?" IDNO noreboot
    Reboot
  noreboot:

  WriteRegStr HKLM Software\sis\Medienverwaltung InstallLocation $INSTDIR
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
    
    File /r C:\Python26
    File python26.dll
    File install.cmd
    File show.cmd
    File start.cmd
    
    DetailPrint "Downloading and installing runtime environment"
    nsExec::ExecToLog /OEM '"$INSTDIR\install.cmd"'
    call checkRetVal

    ;Create shortcuts
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Start Webserver.lnk" "$INSTDIR\start.cmd"
    !insertmacro MUI_STARTMENU_WRITE_END
    
#        File "..\Medienverwaltung.exe"
#        File "..\*.metaDatatypes"
#        File "..\*.SnapshotProperties"


SectionEnd
