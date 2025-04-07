from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class Movie(models.Model):
        
    # _name: El identificador técnico del modelo en Odoo (tabla en la base de datos)
    # _description: Descripción legible para usuarios
    # _order: Define el orden predeterminado de los registros (películas ordenadas por ranking descendente)
    
    _name = 'movie.movie'
    _description = 'Modelo para almacenar información de películas'
    _order = 'ranking desc'
        
    #     Define dos campos obligatorios:
    # name: Campo de texto para el título de la película
    # ranking: Campo numérico decimal para la puntuación de la película

    name = fields.Char(string='Título', required=True)
    ranking = fields.Float(string='Ranking', required=True)
    
    # El decorador @api.model indica que este método se ejecuta a nivel del modelo,
    # no de un registro específico. Esto es adecuado para operaciones como importación de datos.
    
    @api.model
    def fetch_movie_from_api(self):
        """
        Método para consultar la API externa y registrar una nueva película.
        Este método es llamado por el cron job definido en data/cron.xml.
        """
        try:
            # Accede a los parámetros de configuración del sistema con privilegios de administrador
            # Obtiene la URL de la API y la clave API de los parámetros del sistema (configurados en la interfaz de Odoo)
            # Obtener parámetros del sistema
            ICPSudo = self.env['ir.config_parameter'].sudo()
            api_url = ICPSudo.get_param('movie_management.api_url')
            api_key = ICPSudo.get_param('movie_management.api_key')
            
            # Verificar si los parámetros de la API están configurados
            # Si no están configurados, registrar un error y devolver False
            # Esto es importante para evitar errores al intentar acceder a la API sin la configuración adecuada
            # y para asegurar que el cron job no falle sin razón aparente.
            if not api_url or not api_key:
                _logger.error('Parámetros de API no configurados. Configure URL y API key en los parámetros del sistema.')
                return False
            
            # Construir la URL con el api_key como parámetro de consulta
            # Esto es importante para autenticar la solicitud a la API y obtener los datos correctos.
            # La URL de la API debe incluir el api_key como parte de la consulta para autenticar la solicitud
            full_url = f"{api_url}?api_key={api_key}"
            
            # Realizar la consulta a la API
            # Utilizar requests para hacer la solicitud GET a la API
            _logger.info(f"Consultando API: {full_url}")
            response = requests.get(full_url)
            
            # Verificar si la respuesta es exitosa
            if response.status_code == 200:
                data = response.json()
                _logger.info(f"Respuesta de la API: {data}")
                
                # La API devuelve movie_title y ranking_movie
                if 'movie_title' in data and 'ranking_movie' in data:
                    try:
                        # Convertir el ranking a float y crear un nuevo registro de película
                        # Esto es importante para asegurar que los datos se almacenen correctamente en la base de datos
                        # y para evitar errores de tipo al intentar almacenar datos no válidos.
                        # Crear un nuevo registro de película en la base de datos
                        movie = self.create({
                            'name': data['movie_title'],
                            'ranking': float(data['ranking_movie']),
                        })
                        _logger.info(f"Película '{data['movie_title']}' registrada exitosamente con ranking {data['ranking_movie']}")
                        return True
                    except (ValueError, TypeError) as e:
                        _logger.error(f"Error al convertir los datos: {e}")
                else:
                    _logger.error(f"Estructura de respuesta no esperada: {data}")
            else:
                _logger.error(f"Error al consultar la API. Código de estado: {response.status_code}, Respuesta: {response.text}")
                    
        except Exception as e:
            _logger.error(f"Excepción al consultar la API: {str(e)}")
            
        return False