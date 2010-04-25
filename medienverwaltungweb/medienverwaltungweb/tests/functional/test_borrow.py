from medienverwaltungweb.tests import *
from medienverwaltungweb.tests.functional import *
log = logging.getLogger(__name__)

class TestBorrowController(TestController):
    def setUp(self):
        #~ log.debug("FOLLOW ME: setUp")
        TestController.setUp(self)

        record = model.Medium()
        record.title = u"SomeMedium"
        record.image_data = "foo"
        record.isbn = 'isbn1234'
        #~ record.created_ts = datetime.now()
        #~ record.updated_ts = datetime.now()
        record.media_type_id = 2
        meta.Session.add(record)
        meta.Session.commit()

        borrower = model.Borrower()
        borrower.first_name = u"John Doe"
        meta.Session.add(borrower)

        record = model.BorrowAct()
        record.media_id = 1
        record.borrower_id = 1
        borrower.acts.append(record)

        meta.Session.commit()
        self.assertEqual(1, borrower.id)

    def test_list_borrowers(self):
        response = self.app.get(url(controller='borrow',
                                    action='list_borrowers'))
        assert "<h1>All borrowers</h1>" in response

    def test_add_borrower(self):
        response = self.app.get(url(controller='borrow',
                                    action='add_borrower'))
        assert "<h1>Add new Borrower</h1>" in response

    def test_checkout(self):
        response = self.app.get(url(controller='borrow',
                                action='checkout',
                                id='1'))
        assert "<h1>Borrow" in response

    def test_scanner(self):
        response = self.app.get(url(controller='borrow',
                                action='scanner',
                                id='1'))
        assert "<h1>Checkin/checkout with barcode scanner</h1>" in response

    def test_checkout_post_existing(self):
        response = self.app.post(url(controller='borrow',
                                     action='checkout_post'),
                                 params={'id':'1',
                                         'borrower':'1',
                                         'item_id_1':'1'})

        self.assertEqual('http://localhost/borrow/edit_borrower/1',
                         response.location)
        response2 = self.app.get(response.location)
        assert "borrowed to" in response2
        assert "John Doe" in response2

        record = meta.Session.query(model.Borrower).get(1)
        record.session = meta.Session
        self.assertEqual(2, len(record.acts))

    def test_checkout_post_new(self):
        response = self.app.post(url(controller='borrow',
                                     action='checkout_post'),
                                 params={'borrower':'0',
                                         'item_id_1':'1'})

        self.assertEqual('http://localhost/borrow/add_borrower?media_ids=1',
                         response.location)
        record = meta.Session.query(model.Borrower).get(2)
        self.assertEqual(None, record)

        response = self.app.get(url(controller='borrow',
                                    action='add_borrower_post'),
                                 params={'media_ids':'1',
                                         'first_name':'NewOne'})

        record = meta.Session.query(model.Borrower).get(2)
        self.assertEqual('NewOne', record.first_name)
        self.assertEqual(1, len(record.acts))

    def test_add_borrower_post(self):
        response = self.app.get(url(controller='borrow',
                                    action='add_borrower_post'),
                                 params={'first_name':'AnotherNewOne'})

        record = meta.Session.query(model.Borrower).get(2)
        self.assertEqual('AnotherNewOne', record.first_name)
        self.assertEqual(0, len(record.acts))


    def test_list_borrowers(self):
        record = model.Borrower()
        record.first_name = u"User in a List"
        meta.Session.add(record)
        meta.Session.commit()

        response = self.app.get(url(controller='borrow',
                                    action='list_borrowers'))

        assert "<h1>All borrowers</h1>" in response
        assert "User in a List" in response
        assert "John Doe" in response

    def test_edit_borrower(self):
        response = self.app.get(url(controller='borrow',
                                    action='edit_borrower',
                                    id=1))

        assert "John Doe" in response

    def test_edit_borrower_post(self):
        response = self.app.get(url(controller='borrow',
                                    action='edit_borrower_post',
                                    id=1),
                                 params={'first_name':'Changed',
                                         'last_name':'Doe'})

        record = meta.Session.query(model.Borrower).get(1)
        self.assertEqual('Changed', record.first_name)
        self.assertEqual('Doe', record.last_name)

    def test_show_history(self):
        borrower = meta.Session.query(model.Borrower).get(1)

        record = model.BorrowAct()
        record.media_id = 1
        record.borrower_id = 1
        borrower.acts.append(record)
        meta.Session.commit()

        response = self.app.get(url(controller='borrow',
                                    action='show_history',
                                    id=1))

        assert "<h1>Borrow History</h1>" in response
        assert "SomeMedium" in response

    def test_show_history(self):
        response = self.app.get(url(controller='borrow',
                                    action='checkin_post'),
                                 params={'item_id_1':'1'})

        borrower = meta.Session.query(model.Borrower).get(1)
        self.assertNotEqual(None, borrower.acts[0].returned_ts)

    def test_list_borrowed_media(self):
        borrower = meta.Session.query(model.Borrower).get(1)

        response = self.app.get(url(controller='borrow',
                                    action='list_borrowed_media'))

        assert "<h1>Borrowed Media" in response
        assert "SomeMedium" in response
        assert "John Doe" in response


    def test_scanner_post(self):
        response = self.app.get(url(controller='borrow',
                                    action='scanner_post'),
                                 params={'isbns':'isbn1234'})
        assert "SomeMedium" in response

