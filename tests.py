import pytest

class TestBooksCollector:

    # test_001 - позитивнный, добавление новой книги (книги нет в словаре, длина названия 1-40 символов - 1, 2, 18, 39,
    # 40 символов)
    names = [
        'Я',
        'Мы',
        'Денискины рассказы',
        'Чудесное путешествие Нильса с дикими гу',
        'Чудесное путешествие Нильса с дикими гус'
    ]
    @ pytest.mark.parametrize('book_name', names)
    def test_add_new_book_add_new_book(self, collector, book_name):
        collector.add_new_book(book_name)
        assert len(collector.books_genre) == 1

    # test_002 - негативный, добавление книги, имеющейся в словаре (длина названия 1-40 символов - 18 символов)
    def test_add_new_book_add_same_book(self, collector):
        collector.add_new_book('А зори здесь тихие')
        collector.add_new_book('А зори здесь тихие')
        assert len(collector.books_genre) == 1

    # test_003 - негативный, добавление новой книги с некорректной длиной названия (длина названия НЕ 1-40 символов - 0,
    #  41, 42, 61 символов)
    names = [
        '',
        'Чудесное путешествие Нильса с дикими гуся',
        'Чудесное путешествие Нильса с дикими гусям',
        'Чудесное путешествие Нильса с дикими гусями - Сельма Лагерлёф'
    ]
    @ pytest.mark.parametrize('book_name', names)
    def test_add_new_book_add_book_with_incorrect_name(self, collector, book_name):
        collector.add_new_book(book_name)
        assert len(collector.books_genre) == 0

    # test_004 - позитивнный, установление книге жанра (книга из словаря, жанр из словаря)
    def test_set_book_genre_set_book_genre(self, collector):
        collector.add_new_book('Колобок')
        collector.set_book_genre('Колобок', 'Фантастика')
        assert collector.books_genre['Колобок'] == 'Фантастика'

    # test_005 - негативный, установление книге жанра (книга НЕ из словаря, жанр из словаря)
    def test_set_book_genre_incorrect_name_book(self, collector):
        collector.add_new_book('Колобок')
        collector.set_book_genre('Репка', 'Ужасы')
        assert 'Репка' not in collector.books_genre

    # test_006 - негативный, установление книге жанра (книга из словаря, жанр НЕ из словаря)
    def test_set_book_genre_incorrect_name_genre(self, collector):
        collector.add_new_book('Колобок')
        collector.set_book_genre('Колобок', 'Аудио')
        assert collector.books_genre['Колобок'] == ''

    # test_007 - возврат жанра книги по имени (набор 1 - позитивный - название книги из словаря, набор 2 - негативный -
    # название книги НЕ из словаря)
    data_for_test = [
        ['Колобок', 'Фантастика', 'Колобок', 'Фантастика'],
        ['Дед мазай и зайцы', 'Ужасы', 'Репка', None]
    ]
    @pytest.mark.parametrize('book_name, genre, book_name_give, result', data_for_test)
    def test_get_book_genre_return_genre_in_parametres(self, collector, book_name, genre, book_name_give, result):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name_give) == result

    # test_008 - позитивный - возврат списка книг определенного жанра (список книг определенного жанра)
    def test_get_books_with_specific_genre_return_books_with_specific_genre(self, collector):
        collector.add_new_book('Чук и Гек')
        collector.add_new_book('Азбука')
        collector.add_new_book('Сказки')
        collector.set_book_genre('Чук и Гек', 'Ужасы')
        collector.set_book_genre('Азбука', 'Фантастика')
        collector.set_book_genre('Сказки', 'Ужасы')
        assert len(collector.get_books_with_specific_genre('Ужасы')) == 2

    # test_009 - негативный - возврат списка книг определенного жанра (словарь книг пустой)
    def test_get_books_with_specific_genre_no_books(self, collector):
        assert len(collector.get_books_with_specific_genre('Комедии')) == 0

    # test_010 - негативный - возврат списка книг определенного жанра (жанра нет в списке жанров)
    def test_get_books_with_specific_genre_no_genre(self, collector):
        collector.add_new_book('Чук и Гек')
        collector.set_book_genre('Чук и Гек', 'Ужасы')
        collector.add_new_book('Азбука')
        collector.set_book_genre('Азбука', 'Фантастика')
        assert len(collector.get_books_with_specific_genre('Аудио')) == 0

    # test_011 - позитивный - возврат списка книг
    def test_get_books_genre_return_books_genre(self, collector):
        collector.add_new_book('Айболит')
        collector.set_book_genre('Айболит', 'Мультфильмы')
        collector.add_new_book('Солярис')
        collector.set_book_genre('Солярис', 'Фантастика')
        assert (collector.get_books_genre()['Айболит'] == 'Мультфильмы' and collector.get_books_genre()['Солярис'] ==
                'Фантастика')

    # test_012 - позитивный - возврат списка книг, подходящим детям
    def test_get_books_for_children_return_books_for_children(self, collector):
        collector.add_new_book('Крошка Енот')
        collector.set_book_genre('Крошка Енот', 'Мультфильмы')
        collector.add_new_book('Черная комната')
        collector.set_book_genre('Черная комната', 'Ужасы')
        collector.add_new_book('Красная шапочка')
        collector.set_book_genre('Красная шапочка', 'Комедии')
        assert ('Черная комната' not in collector.get_books_for_children()
                and 'Крошка Енот', 'Красная шапочка' in collector.get_books_for_children())

    # test_013 - добавление книги в избранное (набор 1 позитивный - название книги из словаря, в избранном отсутствует,
    # набор 2 негативный - название книги НЕ из словаря, в избранном отсутвует, набор 3 негативный - название книги
    # из словаря, в избранном уже присутствует)
    data_for_test = [
        ['500 пирогов', '100 салатов', '100 салатов', 2],
        ['500 пирогов', '100 салатов', '123 коктейля', 1],
        ['500 пирогов', '100 салатов', '500 пирогов', 1]
    ]
    @pytest.mark.parametrize('book_1, book_2, book_3, result', data_for_test)
    def test_add_book_in_favorites_add_book_in_parametres(self, collector, book_1, book_2, book_3, result):
        collector.add_new_book(book_1)
        collector.add_new_book(book_2)
        collector.add_book_in_favorites(book_1)
        collector.add_book_in_favorites(book_3)
        assert len(collector.favorites) == result

    # test_014 - удаление книги из избранного (набор 1 - позитивный - название книги в изюранном присутствует,
    # набор 2 - негативный - название книги в избранном отсутвует)
    data_for_test = [
        ['500 пирогов', '500 пирогов', 0],
        ['500 пирогов', '100 салатов', 1],
    ]
    @pytest.mark.parametrize('book_name_1, book_name_2, result', data_for_test)
    def test_delete_book_from_favorites_delete_book_in_parametres(self, collector, book_name_1, book_name_2, result):
        collector.add_new_book(book_name_1)
        collector.add_book_in_favorites(book_name_1)
        collector.delete_book_from_favorites(book_name_2)
        assert len(collector.favorites) == result

    # test_015 - позитивный - возврат списка избранных книг
    def test_get_list_of_favorites_books_return_list_of_favorites_books(self, collector):
        collector.add_new_book('Дэнс дэнс дэнс')
        collector.add_book_in_favorites('Дэнс дэнс дэнс')
        assert collector.get_list_of_favorites_books() == ['Дэнс дэнс дэнс']

    # test_016 - позитивный - у добавленной книги нет жанра
    def test_add_new_book_no_genre(self, collector):
        collector.add_new_book('Проверка микрофона')
        assert collector.books_genre['Проверка микрофона'] == ''
