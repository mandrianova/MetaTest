<template>
  <b-list-group-item>
    <b-avatar variant="dark" v-if="doctor.photo && doctor.photo.small_source_url" v-bind:src="doctor.photo.small_source_url" class="mr-3"></b-avatar>
    <b-avatar variant="dark" v-else class="mr-3" :text="get_initials()"></b-avatar>
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
  },
  methods: {
    get_initials () {
      const nameList = this.doctor.name.split(' ').slice(0, 2)
      return nameList.reduce((result, current) => result + current[0], '')
    }
  }
}

</script>
