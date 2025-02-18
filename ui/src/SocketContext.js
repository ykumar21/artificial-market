import React, { createContext, useContext, useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const SocketContext = createContext();

export const useSocket = () => {
    return useContext(SocketContext);
};

export const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const SOCKET_URL = 'http://localhost:8000'; // Adjust to your backend URL

    useEffect(() => {
        const newSocket = io(SOCKET_URL);
        setSocket(newSocket);
        newSocket.on('connect', () => {
            console.log('Socket connected');
        });
        newSocket.on('disconnect', () => {
            console.log('Socket disconnected');
        });
        // Cleanup on unmount
        return () => {
            newSocket.disconnect();
        };
    }, [SOCKET_URL]);
    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};