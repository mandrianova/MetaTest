<template>
  <b-list-group>
    <DoctorListItem
      v-for="(doctor, i) of doctors" :key="doctor.id"
      v-bind:doctor="doctor"
      v-bind:index="i"
    />
  </b-list-group>
</template>

<script>
import DoctorListItem from '@/components/DoctorListItem'
export default {
  props: ['doctors'],
  components: {
    DoctorListItem
  }
}
</script>
