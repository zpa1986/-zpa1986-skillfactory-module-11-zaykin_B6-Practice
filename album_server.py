from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError
import album
@route("/albums/<artist>")
def albums(artist):
    """ в переменную albums_list записываем таблицу найденных альбомов
    для этого обращаемся к функции find(), которую мы написали
    в модуле album
    """
    albums_list=album.find(artist)
    if not albums_list:
        message="Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {} <br>".format(artist)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def make_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")
    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Год альбома введен неверно!")
    try:
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:
        print("Новый альбом с ID #{} успешно сохранен!".format(new_album.id))
        result = "Альбом с ID #{} успешно сохранен".format(new_album.id)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)