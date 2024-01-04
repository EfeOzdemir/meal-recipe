<template>
    <Header />
    <h2 class="text-center text-5xl font-bold mt-10">Info Charts</h2>
    <div class="grid grid-cols-2 mt-10">
        <div class="chart m-auto" v-if="!loading">
            <Bar :data="info" :options="options" />
        </div>
        <div class="chart m-auto" v-if="!loading">
            <Bar :data="comments" :options="options" />
        </div>
    </div>
</template>

<script setup>
import Header from '~/components/admin/Header.vue';
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

//Category counts,
const info = ref({})
const comments = ref({})

const loading = ref(true)

const getInfo = async () => {
    const data = await $fetch('http://localhost:5000/admin/infos')
    info.value.labels = []
    info.value.datasets = [{
        label: 'Category Counts', data: [], backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
        ],
        borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
        ],
        borderWidth: 1
    }]

    for (let i of data) {
        info.value.labels.push(i['category_name'])
        info.value.datasets[0].data.push(i['count'])
    }
}

const getComments = async () => {
    const data = await $fetch('http://localhost:5000/admin/infos/comment')
    comments.value.labels = []
    comments.value.datasets = [{
        label: 'Comment Counts', data: [], backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
        ],
        borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
        ],
        borderWidth: 1
    }]

    console.log(data)
    for (let i of data) {
        comments.value.labels.push(i['recipe_name'])
        comments.value.datasets[0].data.push(i['count'])
    }
}


const chartData = {
    labels: ['January', 'February', 'March'],
    datasets: [{ data: [40, 20, 12] }]
}

const options = {
    responsive: true
}

onMounted(async () => {
    await getInfo()
    await getComments()
    loading.value = false
})

</script>
