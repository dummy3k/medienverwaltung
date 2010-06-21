Imports Microsoft.Win32
Imports CookComputing.XmlRpc
Imports System.Media

Public Class frmMain
    Private mRegistry As RegistryKey = Registry.CurrentUser.CreateSubKey("Software\" & Application.ProductName)
    Private mPlaySuccess As New SoundPlayer(My.Resources.success)
    Private mPlayFailure As New SoundPlayer(My.Resources.failure)

    Private Sub frmMain_FormClosing(ByVal sender As Object, ByVal e As System.Windows.Forms.FormClosingEventArgs) Handles Me.FormClosing
        mRegistry.SetValue("txtUrl", txtUrl.Text)
        mRegistry.SetValue("txtBarcode", txtBarcode.Text)
    End Sub

    Private Sub frmMain_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        txtUrl.Text = mRegistry.GetValue("txtUrl", "http://127.0.0.1:5000")
        txtBarcode.Text = mRegistry.GetValue("txtBarcode", "9783519221210")
    End Sub

    Private Sub cmdFetch_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles cmdFetch.Click
        Fetch()
    End Sub

    Private Function Fetch() As Boolean
        '978345315232801690
        '9 -> 12

        Dim isbn = txtBarcode.Text.Trim()
        If isbn.StartsWith("9") Then
            isbn = isbn.Substring(0, 13)
        ElseIf isbn.StartsWith("3") Then
            isbn = isbn.Substring(0, 10)
        End If

        If txtBarcode.Text.Trim() = "" Then Return False

        Dim proxy = XmlRpcProxyGen.Create(Of IMvApi)()
        proxy.Url = txtUrl.Text
        Dim result = proxy.AddMediumByISBN(isbn, "Books")
        If Not result("success") Then
            mPlayFailure.PlaySync()
            'MsgBox("Failure: " & result("success"))
            txtBarcode.SelectAll()
            Return False
        End If

        txtTitle.Text = result("title")
        'Beep()
        mPlaySuccess.Play()
        Return True
    End Function

    Private Sub txtBarcode_KeyDown(ByVal sender As Object, ByVal e As System.Windows.Forms.KeyEventArgs) Handles txtBarcode.KeyDown
        If e.KeyCode <> Keys.Return And e.KeyCode <> Keys.Tab Then Return
        e.SuppressKeyPress = True
    End Sub

    Private Sub txtBarcode_KeyUp(ByVal sender As System.Object, ByVal e As System.Windows.Forms.KeyEventArgs) Handles txtBarcode.KeyUp
        If e.KeyCode <> Keys.Return And e.KeyCode <> Keys.Tab Then Return
        e.SuppressKeyPress = True
        If Fetch() Then
            txtBarcode.Text = ""
        End If
    End Sub

    Private Sub txtBarcode_Validating(ByVal sender As System.Object, ByVal e As System.ComponentModel.CancelEventArgs) Handles txtBarcode.Validating
        If txtBarcode.Text.Trim() = "" Then
            e.Cancel = False
            Return
        End If

        If Fetch() Then
            txtBarcode.Text = ""
        End If
        e.Cancel = True
    End Sub
End Class
