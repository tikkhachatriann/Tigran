class Modal{
    constructor(elementId){
        this.element = document.getElementById(elementId);
        this.isOpen = false;
    }

    open(){
        if(!this.isOpen){
            this.element.style.display = "block";
            this.isOpen = true;
        }
    }

    close(){
        if(this.isOpen){
            this.element.style.display = "none";
            this.isOpen = false;
        }
    }

    fetchData(url){
        return fetch(url)
            .then(response => response.text())
            .then(data => {
                this.element.innerHTML = data;
            })
            .catch(error => {
                console.error("Error fetching modal content", error)
            })
    }
}


class ReserveModal extends Modal{
    constructor(elementId){
        super(elementId);
        this.date = null;
        this.eventId = null;
    }

    openModal(date, eventId){
        this.date = date;
        this.eventId = eventId;
        this.close();
        this.fetchData(`/get_reserve_modal/${eventId}/${date}`).then(() => {
            timeModal.close()
            successModal.close()
            this.open();
        });
    }
}

class TimeModal extends Modal{
    constructor(elementId){
        super(elementId);
        this.tableId = null;
    }

    openModal(tableId){
        this.tableId = tableId;
        this.close;
        this.fetchData(`/get_time_modal/${tableId}`).then(() =>{
            reserveModal.close()
            this.open();
        })
    }
}

class SuccessModal extends Modal{
    openModal(){
        const timeInput = document.querySelector(
            '#tableBookingModal input[name="time"]'
        );
        const guestsInput = document.querySelector(
            '#tableBookingModal input[name="guests"]'
        );
        const bookingData = {
            eventId: reserveModal.eventId,
            tableId: timeModal.tableId,
            date: reserveModal.date,
            time: timeInput.value,
            guests: guestsInput.value
        }
        this.close();
        const queryParams = new URLSearchParams(bookingData);
        const url = `/get_booking_data?${queryParams}`;
        this.fetchData(url).then(() => {
            timeModal.close();
            this.open();
        });
    }
}

const reserveModal = new ReserveModal("reserveTable");
const timeModal = new TimeModal("tableBookingModal");
const successModal = new SuccessModal("bookingSuccess");