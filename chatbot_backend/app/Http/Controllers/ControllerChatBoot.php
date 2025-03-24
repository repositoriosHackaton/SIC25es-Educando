<?php

namespace App\Http\Controllers;

use App\Models\Conversacion;
use App\Models\Mensajes;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class ControllerChatBoot extends Controller
{

    public function registrarUsuario(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required',
            'password' => 'required|string|min:6',
        ]);

        $usuario = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password), // encriptado
        ]);

        return response()->json([
            'success' => true,
            'usuario' => $usuario,
        ]);
    }


    public function loginUsuario(Request $request)
    {
      
        $request->validate([
            'email' => 'required',
        ]);


        $usuario = User::where('email', $request->email)->first();

        if ($usuario) {
            Auth::login($usuario);

            return response()->json([
                'success' => true,
                'usuario' => $usuario,
            ]);
        }

        return response()->json([
            'success' => false,
            'message' => 'Usuario no encontrado.',
        ], 401);
    }

 

    public function iniciarConversacion(Request $request)
    {
        // ejecutamos dentro de una transaccion
        DB::beginTransaction();
        try {

            $mensaje = $request->input('mensaje');
            $id_usuario = $request->input("id_usuario");
            $usuario = $request->input("usuario");
            $id_conversacion = $request->input("id_conversacion");
            $key_forms = $request->input("dataForm");

            // validamos si id_conversacion es null entonces creamos un nuevo registro
            if ($id_conversacion == null) {
                $nueva_conver = Conversacion::create([
                    'usuario_id' => $id_usuario,
                ]);

                $id_conversacion = $nueva_conver->id;
            }

          
            Mensajes::create([
                'conversacion_id' => $id_conversacion,
                'mensaje' => $mensaje,
                'actor' => $usuario,
            ]);



            if($key_forms){
                $mensaje .= " valor 1: " . $key_forms['valor1'] . " valor 2: " . $key_forms['valor1'];
            }

            // hacemos peticion a la api de python
            $response = Http::post('https://chatboot-production-9c1c.up.railway.app/HipertensoBot', [
                'mensaje' => $mensaje
            ]);

            // obtenemos respuesta de la api de chat boot
            $respuestaBot = $response->json()['mensaje'] ?? 'Error en la respuesta';
            $tipo_usuario = $response->json()['tipo_usuario'];

            Mensajes::create([
                'conversacion_id' => $id_conversacion,
                'mensaje' => $respuestaBot,
                'actor' => $tipo_usuario,
            ]);
            DB::commit();

            // devolvemos respuesta al frontend
            return response()->json([
                'success' => true,
                'mensaje' => $respuestaBot,
                'tipo_usuario' => $tipo_usuario,
                'id_conversacion' => $id_conversacion
            ]);
        } catch (\Exception $e) {
            DB::rollBack();

            return response()->json([
                'success' => false,
                'error' => $e->getMessage(),
            ], 500);
        }
    }

    public function getConversaciones(Request $request)
    {
        $id_usuario = $request->id_usuario;

        $conversacion = Conversacion::where('usuario_id', $id_usuario)->get();
        return response()->json($conversacion);
    }

    public function getConversacion(Request $request)
    {
        try {
    
            $id_conversacion = $request->id_conversacion;

            $conversacion = Mensajes::where('conversacion_id', $id_conversacion)->orderBy('id', 'ASC')->get();
            return response()->json($conversacion);
        } catch (\Throwable $th) {
            return response()->json([
                'success' => false,
            ], 500);
        }
    }
}
