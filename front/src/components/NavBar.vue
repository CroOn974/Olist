<template>
<div class="navbar bg-base-100">
  <div class="flex-1">
    <a class="btn btn-ghost normal-case text-xl">Olist</a>
  </div>
  <div class="flex-none">
    <ul class="menu menu-horizontal px-1">
        <li><button>Import</button></li>
        <li><button>Login</button></li>
        <li><button>Logout</button></li>
    </ul>
  </div>
</div>
</template>

<script>
    export default {
        name: 'NavBar',
    }
</script>