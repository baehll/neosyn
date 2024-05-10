<template>
  <div class="login flex flex-col justify-center items-center h-full">
    <a
      href="/auth/facebook"
      class="inline-flex items-center grow-0 bg-[#0866FF] rounded-md text-white py-4 px-2"
    >
      <svg class="inline-block custom-fill mr-2 " width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_3589_203)">
          <mask id="mask0_3589_203" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="-5" y="-5" width="34" height="34">
            <path d="M-4.8 -4.80005H28.8V28.7999H-4.8V-4.80005Z" fill="white"/>
          </mask>
          <g mask="url(#mask0_3589_203)">
            <path d="M24 12C24 5.3726 18.6274 9.53674e-06 12 9.53674e-06C5.37259 9.53674e-06 0 5.3726 0 12C0 17.6278 3.87432 22.3499 9.10109 23.6466V15.667H6.62659V12H9.10109V10.4199C9.10109 6.33548 10.9495 4.44236 14.9594 4.44236C15.7196 4.44236 17.0314 4.5914 17.568 4.74049V8.06468C17.2848 8.03487 16.7929 8.01994 16.1817 8.01994C14.214 8.01994 13.4538 8.76529 13.4538 10.7031V12H17.3734L16.7001 15.667H13.4538V23.9121C19.3955 23.1945 24 18.1353 24 12Z" fill="white"/>
            <path d="M16.7 15.667L17.3734 12H13.4538V10.7031C13.4538 8.76524 14.214 8.01995 16.1817 8.01995C16.7929 8.01995 17.2848 8.03483 17.568 8.06464V4.7405C17.0314 4.59141 15.7196 4.44232 14.9594 4.44232C10.9495 4.44232 9.10107 6.33549 9.10107 10.4199V12H6.62657V15.667H9.10107V23.6466C10.0295 23.8769 11.0003 24 12 24C12.4922 24 12.9772 23.9697 13.4538 23.9121V15.667H16.7Z" fill="#0866FF"/>
          </g>
        </g>
        <defs>
          <clipPath id="clip0_3589_203">
            <rect width="24" height="24" fill="white"/>
          </clipPath>
        </defs>
      </svg>
      <span>
        Continue with Facebook
      </span>
    </a>
  </div>
</template>
<script>

export default {
  name: 'Login',
  components: {
  },
  data: () => {
    return {
    }
  },
  computed: {
  },
  methods: {
  },
  created: function() {

  }
}
</script>

<style lang="scss">
html{
  #app {
    height: 100vh;
  }

  @media (min-width: 1024px) and (max-width: 1530px) {
    -moz-transform: scale(0.8, 0.8);
    -ms-transform: scale(0.8);
    -webkit-transform: scale(0.8);
    transform: scale(0.8);

    width:125%; /* to compensate for the 0.8 scale */
    transform-origin:0 0; /* to move it back to the top left of the window */
    #app {
      height: 125vh;
    }
  }
}
.login {
}
</style>
