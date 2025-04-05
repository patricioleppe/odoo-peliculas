from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class Movie(models.Model):
    _name = 'movie.movie'
    _description = 'Modelo para almacenar información de películas'
    _order = 'ranking desc'

    name = fields.Char(string='Título', required=True)
    ranking = fields.Float(string='Ranking', required=True)
    
    @api.model
    def fetch_movie_from_api(self):
        """
        Método para consultar la API externa y registrar una nueva película.
        Este método es llamado por el cron job definido en data/cron.xml.
        """
        try:
            # Obtener parámetros del sistema
            ICPSudo = self.env['ir.config_parameter'].sudo()
            api_url = ICPSudo.get_param('movie_management.api_url')
            api_key = ICPSudo.get_param('movie_management.api_key')
            
            if not api_url or not api_key:
                _logger.error('Parámetros de API no configurados. Configure URL y API key en los parámetros del sistema.')
                return False
            
            # Construir la URL con el api_key como parámetro de consulta
            full_url = f"{api_url}?api_key={api_key}"
            
            # Realizar la consulta a la API
            _logger.info(f"Consultando API: {full_url}")
            response = requests.get(full_url)
            
            # Verificar si la respuesta es exitosa
            if response.status_code == 200:
                data = response.json()
                _logger.info(f"Respuesta de la API: {data}")
                
                # La API devuelve movie_title y ranking_movie
                if 'movie_title' in data and 'ranking_movie' in data:
                    try:
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