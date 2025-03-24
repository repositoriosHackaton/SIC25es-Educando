<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Mensajes extends Model
{
    use HasFactory;

    protected $table = 'mensajes';

    protected $fillable = [
        'conversacion_id',
        'mensaje',
        'actor'
    ];
}
