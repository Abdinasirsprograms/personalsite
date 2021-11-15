const menuButton = document.querySelector(".hamburger_button")
const animation_classes = ['top_bun_slide_down', 'slide-right', 
    'bottom_bun_slide_up']
const link_container = document.querySelector(".link_container")
const hamburger_svg = document.querySelector(".hamburger")

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
                }
            } else {
                class_list.add(animation_classes[i])
                if (i === hamburger.length - 1){
                    link_container.classList.add("animate_menu")
                    document.body.style.overflow="hidden"
                }
        }});
}