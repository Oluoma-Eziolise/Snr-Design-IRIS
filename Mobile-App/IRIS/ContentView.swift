//
//  ContentView.swift
//  IRIS
//
//  Created by Divine Eziolise on 2/13/25.
//

import SwiftUI

struct ContentView: View {
    @Environment(\.openURL) var openLink
    var body: some View {
        ZStack{
            Color.teal.opacity(0.3)
                .ignoresSafeArea()
            VStack{
                Button("View Images") {
                    openLink(URL(string: "https://iris-ks91.onrender.com")!)
                    
                }
                .buttonStyle(.borderedProminent)
                .tint(.teal)
                
                
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
