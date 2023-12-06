import { defineStore } from "pinia";
import { ref } from "vue";
import "bootstrap"


export const useGeneralStore = defineStore("gn", () => {
    const infoModalActive = ref(false)
    const infoModal = ref(null)

    function initInfoModal() {
        infoModal.value = new bootstrap.Modal("#loadingModal")
    }

    function showLoadingScreen() {
        if(infoModal.value){
            infoModalActive.value = true
            infoModal.value.show()
            console.log("showing")
        }
    }

    function hideLoadingScreen() {
        if(infoModal.value) {
            infoModal.value.hide()
            infoModalActive.value = false
            console.log("hiding")
        }
    }   

    return {
        hideLoadingScreen,
        showLoadingScreen,
        infoModalActive,
        initInfoModal
    }
})