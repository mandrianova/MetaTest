<template>
  <b-list-group-item>
    <b-avatar variant="dark" v-bind:src="doctor.photo.small_source_url" class="mr-3"></b-avatar>
    <router-link v-bind:to="'doctor/' + doctor.id">
      {{doctor.name}}
    </router-link>

  </b-list-group-item>
</template>

<script>
export default {
  props: {
    doctor: {
      type: Object,
      required: true
    },
    index: Number
  }
}

</script>
