package com.example.myapplication.utils.data

import com.squareup.moshi.JsonClass


@JsonClass(generateAdapter = true)

data class CheckDeviceResponse(
    val login: String
)
