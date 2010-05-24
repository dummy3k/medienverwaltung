Imports CookComputing.XmlRpc

<XmlRpcUrl("http://127.0.0.1:5000/api")> _
Public Interface IMvApi
    Inherits IXmlRpcProxy

    <XmlRpcMethod("AddMediumByISBN")> _
    Function AddMediumByISBN(ByVal isbn As String, ByVal type As String) As XmlRpcStruct
End Interface
