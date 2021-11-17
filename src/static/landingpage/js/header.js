const menuButton = document.querySelector(".hamburger_button")
const animation_classes = ['top_bun_slide_down', 'slide-right', 
    'bottom_bun_slide_up']
const link_container = document.querySelector(".link_container")
const hamburger_svg = document.querySelector(".hamburger")
const title = document.querySelector("h1")

if (menuButton){
    menuButton.addEventListener('click', openHamburger)
}

function openHamburger(e) {
    // convert htmlCollection objects to an array
    hamburger = [...hamburger_svg.children]
    hamburger.forEach((e,i) => {
        let class_list = e.classList
        if (class_list.contains(animation_classes[i])){
            // reverse the animation
            title.style.animationDelay = "750ms"
            hamburger_svg.parentNode.style.animationDelay = "750ms"
            e.getAnimations()[0].playbackRate = -1
            e.getAnimations()[0].onfinish = function() {
                class_list.remove(animation_classes[i])
            }
            if (i === hamburger.length - 1){
                link_container.getAnimations()[0].playbackRate = -1
                link_container.getAnimations()[0].onfinish = function() {
                    link_container.classList.remove("animate_menu")
                    document.body.style.overflow = null        
                }
                hamburger_svg.parentNode.getAnimations()[0].playbackRate = -1
                title.getAnimations()[0].playbackRate = -1
                hamburger_svg.parentNode.getAnimations()[0].onfinish = function(){
                    title.style.animationDelay = null
                    hamburger_svg.parentNode.style.animationDelay = null
                    hamburger_svg.parentNode.classList.remove("active_menu")
                    title.classList.remove("active_menu");
                }
            }
        } else {
            class_list.add(animation_classes[i])
            if (i === 0){
                title.style.animationDelay = null
                hamburger_svg.parentNode.style.animationDelay = null
                hamburger_svg.parentNode.classList.add("active_menu")
                title.classList.add("active_menu");
            }
            if (i === hamburger.length - 1){
                link_container.classList.add("animate_menu")
                document.body.style.overflow="hidden"
            }
    }})
}