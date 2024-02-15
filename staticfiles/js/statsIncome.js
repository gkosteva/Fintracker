const chart = document.querySelector("#container")
const notFound = document.querySelector("#noDataFound")

const categories = {
    salary: {
        name: 'Salary',
        color: '#FE2371'
    },
    rent: {
        name: 'Rent',
        color: '#544FC5'
    },
    bonus: {
        name: 'Bonus',
        color: '#6B8ABC'
    },
    investments: {
        name: 'Investments',
        color: '#00A6A6'
    },
    gifts: {
        name: 'Gifts',
        color: '#D498FB'
    }
}

const getData = (categoryList) => points => points.map(point => ({
    name: point.name,
    y: point.value,
    color: categories[point.name.toLowerCase()].color
}));

const months = [
    document.querySelector("#jan"),
    document.querySelector("#feb"),
    document.querySelector("#march"),
    document.querySelector("#april"),
    document.querySelector("#may"),
    document.querySelector("#june"),
    document.querySelector("#july"),
    document.querySelector("#august"),
    document.querySelector("#sept"),
    document.querySelector("#oct"),
    document.querySelector("#nov"),
    document.querySelector("#dec")
];

function convertResponse(response) {
    const dataprev = [];

    for (const month in response) {
        if (response.hasOwnProperty(month)) {
            const categories = response[month];
            const categoryArray = [];

            for (const category in categories) {
                if (categories.hasOwnProperty(category)) {
                    const amount = categories[category];
                    categoryArray.push({[category]: amount});
                }
            }

            dataprev.push({[month]: categoryArray});
        }
    }

    return dataprev;
}

months.forEach(month => {
    month.addEventListener('click', (e) => {
        console.log(month.textContent)
        fetch(`/incomes/income_category_summary/${month.textContent}`)
            .then((res) => res.json())
            .then((data) => {
                console.log(data)
                dataprev = convertResponse(data)
                const monthData = dataprev[0];
                const monthName = Object.keys(monthData)[0];
                const categoryArray = monthData[monthName];
                const categoryList = [];
                categoryArray.forEach(categoryObject => {
                    const categoryName = Object.keys(categoryObject)[0];
                    const categoryValue = categoryObject[categoryName];
                    categoryList.push({name: categoryName, value: categoryValue});
                });
                if (categoryList.length > 0) {
                    chart.style.display = "block"
                    notFound.style.display = "none"

                    console.log(categoryList)

                    const chartsData = [];
                    categoryList.forEach(current => {
                        chartsData.push({
                            name: current.name,
                            y: current.value,
                            color: categories[current.name.toLowerCase()].color
                        })
                    })

                    console.log(chartsData)

                    Highcharts.chart('container', {
                        chart: {
                            type: 'pie'
                        },
                        title: {
                            text: 'Income summary for ' + month.textContent,
                            align: 'left'
                        },
                        xAxis: {
                            type: 'category'
                        },
                        yAxis: {
                            title: {
                                text: 'Money'
                            }
                        },
                        legend: {
                            enabled: false
                        },
                        tooltip: {
                            shared: true,
                            pointFormat: '<span style="color:{point.color}">\u25CF</span> ' +
                                '{series.name}: <b>{point.y} </b><br/>'
                        },
                        series: [{
                            name: monthName,
                            data: chartsData
                        }]
                    });
                } else {
                    chart.style.display = "none"
                    notFound.style.display = "block"
                }


            })
    })

})



