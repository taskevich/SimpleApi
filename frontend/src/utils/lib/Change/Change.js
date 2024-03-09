export const change = (e, state, setState) => {
    try {
        const {name, value} = e.target
        setState({...state, [name]: value})
    }
    catch (error) {
        console.log(error)
    }
}