document.getElementById('scheduleForm').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('scheduleResult').innerHTML = ""

    const departure = document.getElementById('departure').value.trim();
    const arrival = document.getElementById('arrival').value.trim();

    if (departure === '' || arrival === '') {
        alert('Пожалуйста, заполните все поля.');
        return;
    }

    // Здесь можно добавить логику для получения расписания с сервера
    // Например, используя fetch или XMLHttpRequest

    fetch('/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "departure": departure,
            "arrival": arrival
        }),
    })
        .then(response => {
            return response.json()
        })
        .then(data => {
            document.getElementById('scheduleResult').innerHTML = data.value;
        })
        .catch(error => {
            document.getElementById('scheduleResult').innerHTML = error.error;
        })




    //
    // // Пример статического расписания
    // const schedule = [
    //     { time: '08:00', train: 'Электричка 1' },
    //     { time: '09:30', train: 'Электричка 2' },
    //     { time: '11:00', train: 'Электричка 3' }
    // ];
    //
    // let resultHTML = '<h2>Расписание для маршрута ' + departure + ' - ' + arrival + '</h2>';
    // resultHTML += '<ul>';
    // schedule.forEach(item => {
    //     resultHTML += '<li>' + item.time + ' - ' + item.train + '</li>';
    // });
    // resultHTML += '</ul>';
    //
    // document.getElementById('scheduleResult').innerHTML = resultHTML;
});