from tkinter import *
from tkinter import ttk
_pasos = 80
_dimension = 640


 
damas = Tk()
damas.title("DAMAS CRACK, MAQUINA, LEYENDA")
tablero = Canvas(damas, width=_dimension, height=_dimension)
damas.geometry('640x640')
tablero.place(x=0, y=0)
fichazul = PhotoImage(file='ficha1.png')
fichamarilla = PhotoImage(file='ficha2.png')

turno= "j1"
nombreJugador1 = "Jonathan"
nombreJugador2 = "Chantal"

turnoJugadorLabel=ttk.Label(damas,text="")
turnoJugadorLabel.place(x="625", y="50")

def turnoj():

	turno="Turno de: "
	if turno=="j1":
		turno+=nombreJugador1
	else:
		turno+=nombreJugador2
		turnoJugadorLabel.config(text=turno)

_lista = []
_posicionar = {} 
_index = 0 
_datos_act = {"item":None,"px":0,"py":0}
_posazul = [];
_posamarillo = [];

obj = tablero.create_rectangle(0,0,_dimension,_dimension, outline="blue", fill="white")

for i in range(8):
	for j in range(8):
		pi = i*_pasos
		pj = j*_pasos
		if _index % 2 == 0: 
			if j % 2==0:
				if _index<=2: 			
					obj = tablero.create_image(pj,pi, anchor = NW, image=fichamarilla,tags=("amarilla","ficha")) 
					_posicionar[str(pj)+"-"+str(pi)] = obj
					_posicionar[str(obj)] = {"px":pj,"py":pi}
				else:
					if _index<=4: 	
						pass	
					else: 
						obj = tablero.create_image(pj,pi, anchor = NW, image=fichazul,tags=("azul","ficha"))
						_posicionar[str(pj)+"-"+str(pi)] = obj
						_posicionar[str(obj)] = {"px":pj,"py":pi}
			else:
				obj = tablero.create_rectangle(pj,pi,pj+_pasos,pi+_pasos, outline="black", fill="black")
		else:
			if j % 2!=0:
				if _index<=2: 
					obj = tablero.create_image(pj,pi, anchor = NW, image=fichamarilla,tags=("amarilla","ficha"))
					_posicionar[str(pj)+"-"+str(pi)] = obj
					_posicionar[str(obj)] = {"px":pj,"py":pi}
				else:
					if _index<=4: 	
						pass			
					else: 
						obj = tablero.create_image(pj,pi, anchor = NW, image=fichazul,tags=("azul","ficha"))
						_posicionar[str(pj)+"-"+str(pi)] = obj
						_posicionar[str(obj)] = {"px":pj,"py":pi}
			else:
				obj = tablero.create_rectangle(pj,pi,pj+_pasos,pi+_pasos, outline="black", fill="black")
		 
		_lista.append(obj)
	_index+=1 

for _key in _posicionar:
	print(_key,_posicionar[_key])
 
sign = lambda x: (1, -1)[x < 0]




def buttonClick(event):
	pass
def buttonPress(event):

	global _datos_act
	_item = tablero.find_closest(event.x, event.y)[0] 
	_tags = tablero.gettags(_item)
	if "ficha" in _tags:
		_item_key = str(_item)
		_val = _posicionar.get(_item_key,None)
		if _val is not None:
			_datos_act["item"] = _item
			floorX = event.x - (event.x % _pasos)
			floorY = event.y - (event.y % _pasos) 
			_datos_act["px"] = event.x
			_datos_act["py"] = event.y  
			_datos_act["fpx"] = floorX
			_datos_act["fpy"] = floorY 
			_datos_act["relativeOffsetX"] = event.x-_val["px"]
			_datos_act["relativeOffsetY"] = event.y-_val["py"]
		else:
			pass
	else:
		_datos_act["item"] = None 
	



def buttonRelease(event):
	global _posicionar
	global _datos_act
	global tablero
	_item = _datos_act["item"]
	if _item is None:
		return
	_px = _datos_act["px"]
	_py = _datos_act["py"]

	_fpx = _datos_act["fpx"]
	_fpy = _datos_act["fpy"]
	_item_key = str(_item)
	_last_pos = _posicionar.get(_item_key,None) 
	_lpx = _last_pos["px"]
	_lpy = _last_pos["py"] 
	_tags = tablero.gettags(_item)
	_items = tablero.find_overlapping(event.x, event.y,event.x, event.y) 
	print(_items)
	if _items[1]!=1:
		floorX = event.x - (event.x % _pasos)
		floorY = event.y - (event.y % _pasos) 
		_key = str(floorX)+"-"+str(floorY)
		deltaFloorX = floorX - _fpx
		deltaFloorY = floorY - _fpy
		abs_deltaFloorX = abs(deltaFloorX)
		abs_deltaFloorY = abs(deltaFloorY)
		if(
			deltaFloorX==0 or 
			deltaFloorY==0 or 
			abs_deltaFloorX!=abs_deltaFloorY or 
			abs_deltaFloorX>160
		):

			_deltaX = _lpx - _px + _datos_act["relativeOffsetX"]
			_deltaY = _lpy - _py + _datos_act["relativeOffsetY"] 
			tablero.move(_item,_deltaX,_deltaY)
			if turno=="j1":
				turno="j2"
			else:
				turno="j1"	
			turnoj()			
		else: 
			if abs_deltaFloorX>80:
				tfloorX = floorX - sign(deltaFloorX) * _pasos
				tfloorY = floorY - sign(deltaFloorY) * _pasos
				_tkey = str(tfloorX)+"-"+str(tfloorY) 
				_t1key = str(floorX)+"-"+str(floorY) 
				_val = _posicionar.get(_tkey,None) 
				_val1 = _posicionar.get(_t1key,None) 
				if _val is None:   

					_deltaX = _lpx - _px + _datos_act["relativeOffsetX"]
					_deltaY = _lpy - _py + _datos_act["relativeOffsetY"] 
					tablero.move(_item,_deltaX,_deltaY)
					if turno=="j1":
						turno="j2"
					else:
						turno="j1"	
					turnoj()					 
				else:  
					if _val1 is None:
						_otags = tablero.gettags(_val)
						if "ficha" in _otags:
							if ("amarilla" in _tags and "azul" in _otags) or ("amarilla" in _otags and "azul" in _tags):
								_deltaX = floorX -_px + _datos_act["relativeOffsetX"]
								_deltaY = floorY - _py + _datos_act["relativeOffsetY"]
								tablero.move(_item,_deltaX,_deltaY)
								_posicionar[_key] = _item
								_last_item_key = str(_posicionar[_item_key]["px"])+"-"+str(_posicionar[_item_key]["py"])
								_posicionar[_last_item_key] = None
								_posicionar[_item_key]["px"]=floorX
								_posicionar[_item_key]["py"]=floorY
								tablero.delete(_val);
								_posicionar[str(_val)] = None
								_posicionar[_tkey] = None 
								if turno=="j1":
									turno="j2"
								else:
									turno="j1"	
								turnoj()								
							else:

								_deltaX = _lpx - _px + _datos_act["relativeOffsetX"]
								_deltaY = _lpy - _py + _datos_act["relativeOffsetY"] 
								tablero.move(_item,_deltaX,_deltaY) 
						else:

							_deltaX = _lpx - _px + _datos_act["relativeOffsetX"]
							_deltaY = _lpy - _py + _datos_act["relativeOffsetY"] 
							tablero.move(_item,_deltaX,_deltaY) 
					else:

						_deltaX = _lpx - _px + _datos_act["relativeOffsetX"]
						_deltaY = _lpy - _py + _datos_act["relativeOffsetY"] 
						tablero.move(_item,_deltaX,_deltaY) 

			else:
				_val = _posicionar.get(_key,None) 
				if _val is not None:   

					_deltaX = _lpx - _px + _datos_act["relativeOffsetX"]
					_deltaY = _lpy - _py + _datos_act["relativeOffsetY"] 
					tablero.move(_item,_deltaX,_deltaY)  
				else:
					_deltaX = floorX -_px + _datos_act["relativeOffsetX"]
					_deltaY = floorY - _py + _datos_act["relativeOffsetY"]
					tablero.move(_item,_deltaX,_deltaY)
					_posicionar[_key] = _item
					_last_item_key = str(_posicionar[_item_key]["px"])+"-"+str(_posicionar[_item_key]["py"])
					_posicionar[_last_item_key] = None
					_posicionar[_item_key]["px"]=floorX
					_posicionar[_item_key]["py"]=floorY

def buttonMotion(event):
	global _datos_act
	global tablero
	_item = _datos_act["item"]
	_px = _datos_act["px"]
	_py = _datos_act["py"]
	_deltaX = event.x - _px
	_deltaY = event.y - _py
	_datos_act["px"] = event.x
	_datos_act["py"] = event.y
	if  _item is not None:
		_tags = tablero.gettags(_item)
		if "ficha" in _tags:
			tablero.tag_raise(_item)
			tablero.move(_item,_deltaX,_deltaY)

 
tablero.tag_bind("ficha","<Button-1>", buttonClick) 
tablero.tag_bind("ficha","<ButtonPress-1>", buttonPress) 
tablero.tag_bind("ficha","<ButtonRelease-1>", buttonRelease) 
tablero.tag_bind("ficha","<B1-Motion>", buttonMotion) 


damas.mainloop()

