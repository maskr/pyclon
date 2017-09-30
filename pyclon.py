import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
class Principal:
	def on_boton_no_clicked(self, *args):
		ventana_verificar.hide()
	def on_boton_si_clicked(self, *args):
		ventana_verificar.hide()
		if not esta_vacio():
			copiar(caja_entrada.get_text(), caja_salida.get_text())
		else:
			etiqueta_info.set_text(msg_caja())
			muestra_info()
	def on_boton_salir_clicked(self, *args):
		Gtk.main_quit(*args)
	def on_boton_seleccionar_destino_clicked(self, *args):
		ventana_destino.show()
	def on_boton_seleccionar_origen_clicked(self, *args):
		ventana_origen.show()
	def on_boton_iniciar_clicked(self, *args):
		ventana_verificar.show()
	def on_boton_origen_abrir_clicked(self, *args):
		caja_entrada.set_text(selector_origen.get_text())
		ventana_origen.hide()
	def on_boton_origen_cancelar_clicked(self, *args):
		ventana_origen.hide()
	def on_boton_selector_destino_ok_clicked(self, *args):
		caja_salida.set_text(selector_destino.get_text())
		ventana_destino.hide()
	def on_boton_selector_destino_cancelar_clicked(self, *args):
		ventana_destino.hide()
	def on_file_selector_origen_file_activated(self, *args):
		selector_origen.set_text(obtener_click_origen())
	def on_file_selector_destino_file_activated(self, *args):
		selector_destino.set_text(obtener_click_destino())
	def on_file_selector_destino_selection_changed(self, *args):
		try:
			selector_destino.set_text(obtener_click_destino())
		except:
			pass
	def on_file_selector_origen_selection_changed(self, *args):
		try:
			selector_origen.set_text(obtener_click_origen())
		except:
			pass
	def on_boton_informacion_clicked(self, *args):
		ventana_informacion.hide()
	def on_boton_info_clicked(self, *args):
		etiqueta_info.set_text(msg_info())
		muestra_info()
def obtener_click_destino():
	seleccion = ventana_destino.get_filename()
	return seleccion
def obtener_click_origen():
	seleccion = ventana_origen.get_filename()
	return seleccion
def muestra_info():
	ventana_informacion.show()
def msg_permisos():
	msg = '''No es posible realizar la operación.

Compruebe que dispone de los permisos
pertinentes.'''
	return msg
def msg_caja():
	msg = '''No es posible realizar la acción.
Verifique la ruta de origen y el destino.'''
	return msg
def msg_fin():
	msg = '''Copia Finalizada.
Tamaño: {}'''
	return msg
def msg_ioerror():
	msg = '''Error de Entrada/Salida.

Copia interrumpida'''
	return msg
def msg_error_generico():
	msg = '''Se ha producido un error.
No se puede continuar.'''
	return msg
def msg_info():
	msg = '''(C)GNU/GPL3,David Crespo'''
	return msg
def esta_vacio():
	if not caja_entrada.get_text() or not caja_salida.get_text():
		return True
	else:
		return False
def copiar(entrada, salida):
	posicion = 0
	barra_progreso.set_value(0)
	try:
		with open(entrada, "rb") as origen:
			origen.seek(0, 2)
			final = origen.tell()
			origen.seek(0, 0)
			destino = open(salida, "wb")
			for i in range(0, final, 1024):
				origen.seek(posicion)
				destino.write(origen.read(1024))
				posicion = posicion + 1024
				barra_progreso.set_value((origen.tell()*1)/final)
				while Gtk.events_pending():
					Gtk.main_iteration()
			origen.close()
			destino.close()
			barra_progreso.set_value(final)
			etiqueta_info.set_text(msg_fin().format(final))
			muestra_info()
	except PermissionError:
		etiqueta_info.set_text(msg_permisos())
		muestra_info()
	except IOError:
		etiqueta_info.set_text(msg_ioerror())
		muestra_info()
	except:
		etiqueta_info.set_text(msg_error_generico())
		muestra_info()
constructor = Gtk.Builder()
constructor.add_from_file("pyclon.glade")
constructor.connect_signals(Principal())
ventana = constructor.get_object("principal")
ventana_verificar = constructor.get_object('verificar')
ventana_origen = constructor.get_object('file_selector_origen')
ventana_destino = constructor.get_object('file_selector_destino')
ventana_informacion = constructor.get_object('informacion')
selector_origen = constructor.get_object('entrada_selector_origen')
selector_destino = constructor.get_object('entrada_selector_destino') 
caja_entrada = constructor.get_object('entrada_origen')
caja_salida = constructor.get_object('entrada_destino')
barra_progreso = constructor.get_object('barra_progreso')
etiqueta_info = constructor.get_object('etiqueta')
ventana.show_all()
Gtk.main()
