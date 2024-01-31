import unittest
from app import app, db, Usuario, Livro, Oferta

class TestYourFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_usuario(self):
        usuario = Usuario(nome='Test', email='test@test.com')
        usuario.set_password('test123')
        db.session.add(usuario)
        db.session.commit()
        self.assertEqual(Usuario.query.count(), 1)


if __name__ == "__main__":
    unittest.main()
