new Vue({
    el: '#edit',
    data: {
        items: [],
        bought_id: null,
        delete_id: null,
        name: null,
        price: null,
        image: null,
        message: null,
    },
    mounted: function() {
        axios({
            method: 'get',
            url: '/api/youritems'
        })
        .then(response => {
            this.items = response.data
        })
    },
    methods: {
        editItem() {
            axios.post('/api/edit',
            {
                name: this.name,
                price: this.price,
                image: this.image,
                bought_id: this.bought_id,
            })
            .then(response => {
                if (response.data == ""){
                    window.location.href = '/edit.html'
                } else {
                    this.message = response.data
                }
            })
        },
        deleteItem() {
            axios.post('/api/delete',
            {
                bought_id: this.delete_id,
            })
            .then(response => {
                window.location.href = '/edit.html'
            })
        },
        logOut() {
            axios.post('/api/logout',
            {
                logged: "0",
            })
            .then(response => {
                localStorage.clear();
                window.location.href = '/login.html'
            })
        },
    },
})