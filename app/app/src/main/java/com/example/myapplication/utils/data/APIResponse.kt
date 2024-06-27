package com.example.myapplication.utils.data

import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)

data class APIResponse(
    val success: Boolean,
    val msg: String,
    val data: String
)
