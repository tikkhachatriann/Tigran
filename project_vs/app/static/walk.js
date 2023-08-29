
class ModalManager {
    constructor() {
        this.date = null;
        this.tableBookingModal = document.getElementById('tableBookingModal');
        this.bookSuccess = document.getElementById('booking-success');
    }

    openTimeModal(date) {
        this.date = date;
        this.toggleDisplay(this.tableBookingModal);
    }

    toggleDisplay(element) {
        element.style.display = (element.style.display === 'none') ? 'block' : 'none';
    }

    bookTable() {

        const timeInput = document.querySelector(
            '#tableBookingModal input[name="time"]'
        );
        const guestsInput = document.querySelector(
            '#tableBookingModal input[name="guests"]'
        );
        const time = timeInput.value;
        const guests = guestsInput.value;

        const bookingData = {
            date: this.date,
            time: time,
            guests: guests
        };

        fetch('/get_booking_data',{  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        })
        .then(response => response.json())
        .then(data => {
            if (data["success"]) {
                renderBookingSuccess(data);            
            } else {
                console.log(data)
                renderBookingError(data["message"]);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function renderBookingSuccess(data) {
    bookSuccess = document.getElementById('booking-success');
    eventElement = document.getElementById("event")
    
    modalObj.openTimeModal(data.date);
    modalObj.toggleDisplay(bookSuccess);

    bookSuccess.innerHTML = `
        <h2>Congratulations You Have Successfully Booked Your Table</h2>
        <p>Date: ${data.date}</p>
        <p>Time: ${data.time} For ${data.guests} people</p>
        <div class="links a-href">
            <a href="{{ url_for('home') }}">Back Home</a>
        </div>
    `;
}

function renderBookingError(message) {
    const errorContainer = document.getElementById('error-message');
    if (errorContainer) {
        errorContainer.innerHTML = message;
        errorContainer.style.display = 'block';
    }
}

let modalObj = new ModalManager();
