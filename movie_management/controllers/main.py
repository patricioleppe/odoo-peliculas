from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)

class MovieController(http.Controller):
    @http.route('/api/top_movies', type='http', auth='public', methods=['GET'], csrf=False)
    def get_top_movies(self, **kwargs):
        """
        Endpoint para obtener las 10 películas con mejor ranking.
        Retorna un JSON con los campos id, título y ranking.
        """
        try:
            #  # Buscar las 10 películas con mejor ranking
            # request.env: Accede al entorno de Odoo desde la petición HTTP
            # ['movie.movie']: Accede al modelo de películas definido anteriormente
            # sudo(): Ejecuta la consulta con privilegios de administrador (evita restricciones de acceso)
            # search([]): Busca todos los registros (array vacío = sin condiciones)
            movies = request.env['movie.movie'].sudo().search([], order='ranking desc', limit=10)
            
            # Transformar los resultados a un formato adecuado para JSON
            result = []
            for movie in movies:
                result.append({
                    'id': movie.id,
                    'title': movie.name,
                    'ranking': movie.ranking
                })
            
            # Retornar los resultados en formato JSON
            return request.make_response(
                json.dumps(result),
                headers=[('Content-Type', 'application/json')]
            )
        
        except Exception as e:
            _logger.error(f"Error al obtener top películas: {str(e)}")
            error_response = {
                'error': 'Error interno del servidor',
                'details': str(e)
            }
            return request.make_response(
                json.dumps(error_response),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
            
            
    @http.route('/api/bad_movies', type='http', auth='public', methods=['GET'], csrf=False)
    def get_bad_movies(self, **kwargs):
        """
        Endpoint para obtener las 10 películas con mejor ranking.
        Retorna un JSON con los campos id, título y ranking.
        """
        try:
            #  # Buscar las 10 películas con mejor ranking
            # request.env: Accede al entorno de Odoo desde la petición HTTP
            # ['movie.movie']: Accede al modelo de películas definido anteriormente
            # sudo(): Ejecuta la consulta con privilegios de administrador (evita restricciones de acceso)
            # search([]): Busca todos los registros (array vacío = sin condiciones)
            movies = request.env['movie.movie'].sudo().search([], order='ranking asc', limit=3)
            
            # Transformar los resultados a un formato adecuado para JSON
            result = []
            for movie in movies:
                result.append({
                    'id': movie.id,
                    'title': movie.name,
                    'ranking': movie.ranking
                })
            
            # Retornar los resultados en formato JSON
            return request.make_response(
                json.dumps(result),
                headers=[('Content-Type', 'application/json')]
            )
        
        except Exception as e:
            _logger.error(f"Error al obtener top películas: {str(e)}")
            error_response = {
                'error': 'Error interno del servidor',
                'details': str(e)
            }
            return request.make_response(
                json.dumps(error_response),
                headers=[('Content-Type', 'application/json')],
                status=500
            )