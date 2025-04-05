{
    'name': 'Gestión de Películas',
    'version': '1.0',
    'summary': 'Módulo para gestionar películas desde API externa',
    'description': """
        Este módulo permite:
        - Consultar una API externa para obtener información de películas
        - Almacenar y gestionar registros de películas
        - Exponer un endpoint REST para obtener el top 10 de películas
    """,
    'category': 'Entertainment',
    'author': 'Tu Nombre',
    'website': 'https://www.ejemplo.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/movie_view.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}