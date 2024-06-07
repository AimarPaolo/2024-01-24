import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self._choiceMethod = None

    def fillDD(self):
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(f"{i}"))
        for method in self._model.getMethods():
            self._view.ddmetodi.options.append(ft.dropdown.Option(data=method, text=method.Order_method_type, on_click=self.readMethod))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        year = self._view.ddyear.value
        s = self._view.txtN.value
        if year is None or self._choiceMethod is None:
            self._view.txt_result.controls.append(ft.Text(f"Selezionare delle opzioni nei dropdown!!"))
            self._view.update_page()
            return
        try:
            s_int = float(s)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"Errore nell'inserimento"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        self._model.buildGraph(year, self._choiceMethod.Order_method_code, s_int)
        nNodes, nEdges = self._model.getCaratteristiche()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nEdges} archi"))

        self._view.update_page()



    def handle_calcola_prodotti(self, e):
        self._view.txt_result.controls.append(ft.Text(f""))
        self._view.txt_result.controls.append(ft.Text(f"------------------------------"))
        self._view.txt_result.controls.append(ft.Text(f""))
        self._view.txt_result.controls.append(ft.Text(f"I prodotti più redditizi sono:"))
        d1, d2 = self._model.getMoreRedditizio()
        print(d1, d2)
        count = 0
        for key, value in d1.items() :
            count += 1
            self._view.txt_result.controls.append(ft.Text(f"Prodotto {key} archi entranti {value} ricavo totale {d2[key]}"))
            if count == 5:
                break
        self._view.update_page()

    def handle_path(self, e):
        pass

    def readMethod(self, e):
        if e.control.data is None:
            self._choiceMethod = None
        else:
            self._choiceMethod = e.control.data
