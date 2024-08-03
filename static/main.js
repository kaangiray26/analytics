const { createApp, ref, onMounted, onBeforeMount } = Vue;

createApp({
    setup() {
        const sites = ref([]);
        const paths = ref([]);
        const top_path_count = ref(1);
        const selected = ref("null");

        const total = ref(0);
        const unique = ref(0);
        var chart = null;

        async function setup() {
            // Get sites data
            const response = await fetch("http://localhost:5000/sites").then(
                (res) => res.json(),
            );
            sites.value = response.sites.map((arr) => arr[0]);
            get_site(sites.value[0]);
        }

        async function get_site(site) {
            const response = await fetch("http://localhost:5000/site", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ site }),
            }).then((res) => res.json());
            console.log(response);

            selected.value = site;
            total.value = response.total;
            unique.value = response.unique;

            // Parse traffic data
            let traffic = Array(12).fill(0);
            response.traffic.map((row) => {
                traffic[parseInt(row[0]) - 1] = row[1];
            });

            // Parse paths data
            if (response.paths.length) {
                top_path_count.value = response.paths[0][1];
                paths.value = response.paths;
            } else {
                top_path_count.value = 1;
                paths.value = [];
            }

            // Change chart data
            chart.data.datasets[0].data = traffic;
            chart.update();
        }

        function get_year() {
            return new Date().getFullYear();
        }

        function format_int(num) {
            if (num === 0) return "0";
            if (num > 1000000000) return (num / 1000000000).toFixed(1) + "B";
            if (num > 1000000) return (num / 1000000).toFixed(1) + "M";
            if (num > 1000) return (num / 1000).toFixed(1) + "K";
            return num;
        }

        onBeforeMount(() => {
            setup();
        });

        onMounted(() => {
            const data = {
                labels: [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ],
                datasets: [
                    {
                        data: [65, 59, 80, 81, 56, 55, 40],
                        label: "Visitors",
                        fill: false,
                        borderColor: "#1c71d8",
                        tension: 0.1,
                    },
                ],
            };

            chart = new Chart(document.getElementById("myChart"), {
                type: "line",
                data: data,
                options: {
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            // defining min and max so hiding the dataset does not change scale range
                            min: 0,
                            max: 100,
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                    },
                },
            });
        });

        return {
            total,
            unique,
            selected,
            sites,
            paths,
            top_path_count,
            get_site,
            get_year,
            format_int,
        };
    },
}).mount("#app");
