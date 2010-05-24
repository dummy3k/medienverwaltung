Imports Microsoft.Win32
Imports CookComputing.XmlRpc

Public Class frmMain
    Private mRegistry As RegistryKey = Registry.CurrentUser.CreateSubKey("Software\" & Application.ProductName)

    Private Sub frmMain_FormClosing(ByVal sender As Object, ByVal e As System.Windows.Forms.FormClosingEventArgs) Handles Me.FormClosing
        mRegistry.SetValue("txtUrl", txtUrl.Text)
        mRegistry.SetValue("txtBarcode", txtBarcode.Text)
    End Sub

    Private Sub frmMain_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        txtUrl.Text = mRegistry.GetValue("txtUrl", "http://127.0.0.1:5000")
        txtBarcode.Text = mRegistry.GetValue("txtBarcode", "9783519221210")
    End Sub

    Private Sub cmdFetch_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles cmdFetch.Click
        Dim proxy = XmlRpcProxyGen.Create(Of IMvApi)()
        proxy.Url = txtUrl.Text
        Dim result = proxy.AddMediumByISBN(txtBarcode.Text, "Books")
        If Not result("success") Then
            MsgBox("Failure: " & result("success"))
            Return
        End If

        txtTitle.Text = result("title")
        'Stop
    End Sub

    Private Sub Label2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs)

    End Sub

    Private Sub TextBox1_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles txtTitle.TextChanged

    End Sub
End Class
