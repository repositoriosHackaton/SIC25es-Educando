<?php

namespace Database\Seeders;
use Carbon\Carbon;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        DB::table('users')->insert([
            [
                'name' => 'Moises Molina',
                'email' => 'Moises',
                'email_verified_at' => null,
                'password' => '$2y$12$G.2hmAYPE8K0vTfaf.xbXe2s56W1c0Oh22QkXPMAmquKvSBOUdOzW',
                'remember_token' => null,
                'created_at' => Carbon::parse('2025-03-25 01:12:14'),
                'updated_at' => Carbon::parse('2025-03-25 01:12:14'),
            ],
            [
                'name' => 'Vilic Ayala',
                'email' => 'Vilic',
                'email_verified_at' => null,
                'password' => '$2y$12$i9F/Vl4qLDqadu37O2Yfb.PlBXJyLT8eTDtAzN46UU8ubEebogy0a',
                'remember_token' => null,
                'created_at' => Carbon::parse('2025-03-25 01:13:00'),
                'updated_at' => Carbon::parse('2025-03-25 01:13:00'),
            ],
            [
                'name' => 'Carlos Pacheco',
                'email' => 'Carlos',
                'email_verified_at' => null,
                'password' => '$2y$12$3.95IWUlcMZFSFRLD8gcROlvBPMohOb5rFO7CCGABewjXXPPkLFY.',
                'remember_token' => null,
                'created_at' => Carbon::parse('2025-03-25 01:13:19'),
                'updated_at' => Carbon::parse('2025-03-25 01:13:19'),
            ],
            [
                'name' => 'Tania Franco',
                'email' => 'Tania',
                'email_verified_at' => null,
                'password' => '$2y$12$GeKWHgh9MyRSuTo.hhQ9M.qSTxxkWK5qJGUorE3DaIBTEM51Ksgq.',
                'remember_token' => null,
                'created_at' => Carbon::parse('2025-03-25 01:13:36'),
                'updated_at' => Carbon::parse('2025-03-25 01:13:36'),
            ],
            [
                'name' => 'Gabriel Duran',
                'email' => 'Gabriel',
                'email_verified_at' => null,
                'password' => '$2y$12$qeUQvcHziFa4FwuFuSqNuefZk89j6Wv37P/Eet2NhOEJiX0tBS7He',
                'remember_token' => null,
                'created_at' => Carbon::parse('2025-03-25 01:14:01'),
                'updated_at' => Carbon::parse('2025-03-25 01:14:01'),
            ],
        ]);
    }
}
