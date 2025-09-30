import {io} from 'socket.io-client';
import APIEndpoint from '../APIEndpoint';
const socket = io(APIEndpoint)
export default socket;