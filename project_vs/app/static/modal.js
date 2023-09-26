class ModalManager{

    constructor(){
        this.date = null;
        this.eventId = null;
        this.tableId = null;
        this.timeModalOpen = false;
        this.reserveModalOpen = false;
        this.successModalOpen = false;
        this.success = document.getElementById("bookingSuccess"); 
        this.reserveModal = document.getElementById("reserveTable");
        this.timeModal = document.getElementById("tableBookingModal");
        
    }

    openReserveModal(date, eventId) {
        this.date = date;
        this.eventId = eventId;
       
        if(this.timeModalOpen){
            this.hideReserveModal();
        }

        if(!this.reserveModalOpen){
            fetch(`/get_reserve_modal/${eventId}`)
                .then(response => response.text())
                .then(data => {
                    this.reserveModal.innerHTML = data;
                    this.hideTimeModal();
                    this.hideSuccessModal();
                    this.showReserveModal();
                })
                .catch(error => {
                    console.error('Error fetching modal content:', error);
                });
        }else{
            this.hideReserveModal()
        }
    }

    openTimeModal(tableId) {
        this.tableId = tableId;

        if(this.reserveModalOpen){
            this.hideReserveModal();
        }
        
        if(!this.timeModalOpen){
            fetch(`/get_time_modal/${tableId}`)
                .then(response => response.text())
                .then(data => {
                    this.timeModal.innerHTML = data;
                    this.showTimeModal();       
                })
                .catch(error => {
                    console.error('Error fetching modal content:', error);
                });
        }else {
            this.hideTimeModal()
        }
    }

    bookingSuccess(){   
        const timeInput = document.querySelector(
            '#tableBookingModal input[name="time"]'
        );
        const guestsInput = document.querySelector(
            '#tableBookingModal input[name="guests"]'
        );

        if (!timeInput.checkVisibility() || !guestsInput.checkVisibility()){  
            const errorMessage = document.querySelector("#error-message");
            errorMessage.textContent = "Please fill out all required fields";
            return;
        }

        const bookingData = {
            eventId: this.eventId,
            tableId: this.tableId,
            date: this.date,
            time: timeInput.value,
            guests: guestsInput.value
        };

        const queryParams = new URLSearchParams(bookingData);
        const url = `/get_booking_data?${queryParams}`;

        if(this.successModalOpen){
            this.hideTimeModal();
        }

        if(!this.successModalOpen){
            fetch(url)
                .then(response => response.text())
                .then(data => {
                    this.success.innerHTML = data;
                    this.hideTimeModal();
                    this.showSuccessModal();    
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }else{
            this.hideSuccessModal();
        }
    }

    showReserveModal(){
        this.reserveModal.style.display = "block";
        this.reserveModalOpen = true;
    }

    hideReserveModal(){
        this.reserveModal.style.display = "none";
        this.reserveModalOpen = false;
    }

    showTimeModal(){
        this.timeModal.style.display = "block";
        this.timeModalOpen = true;
    }

    hideTimeModal(){
        this.timeModal.style.display = "none";
        this.timeModalOpen = false;
    }

    showSuccessModal(){
        this.success.style.display = "block";
        this.successModalOpen = true;
    }

    hideSuccessModal(){
        this.success.style.display = "none";
        this.successModalOpen = false;
    }
}

const modalManager = new ModalManager()


